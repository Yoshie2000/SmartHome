#include <FastLED.h>
#include <SPI.h>
#include "RF24.h"

FASTLED_USING_NAMESPACE

// FastLED "100-lines-of-code" demo reel, showing just a few
// of the kinds of animation patterns you can quickly and easily
// compose using FastLED.
//
// This example also shows one easy way to define multiple
// animations patterns and have them automatically rotate.
//
// -Mark Kriegsman, December 2014

#if defined(FASTLED_VERSION) && (FASTLED_VERSION < 3001000)
#warning "Requires FastLED 3.1 or later; check github for latest code."
#endif

#define DATA_PIN    3
//#define CLK_PIN   4
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB
#define NUM_LEDS    300
CRGB leds[NUM_LEDS];

/* Hardware configuration: Set up nRF24L01 radio on SPI bus plus pins 7 & 8 */
RF24 radio(7, 8);

// THESE ARE THE VARIABLES FOR THE EFFECTS
uint8_t rainbowDeltaHue = 3;

uint8_t glitterChance = 100;

uint8_t confettiPerUpdate = 2;
uint8_t confettiHueRange = 32;

uint8_t sinelonBPM = 20;
uint8_t sinelonFadeSpeed = 10; // in frames

uint8_t bpmBPM = 80;
uint8_t bpmHueOffset = 1;
uint8_t bpmPartCount = 30;
uint8_t bpmColorPaletteIndex = 3;

uint8_t juggleDotCount = 10;
uint8_t juggleDotHueIncrease = 64;
uint8_t juggleFadeSpeed = 10; // in frames

uint8_t hueUpdateDelay = 10; // in ms
uint8_t fps = 120;
uint8_t brightness = 80;

CRGBPalette16 colorPalettes[4] = {
  RainbowColors_p,
  RainbowStripeColors_p,
  PartyColors_p,
  HeatColors_p
};

// Adresses of the devices
uint32_t pipes[2] = { 0xF0E1LL, 0xF0D2LL };

void setup() {
  delay(3000); // 3 second delay for recovery

  Serial.begin(9600);

  FastLED.addLeds<LED_TYPE, DATA_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);

  FastLED.setBrightness(brightness);

  radio.begin();
  radio.enableDynamicPayloads();
  radio.setRetries(5, 15);
  radio.setPALevel(RF24_PA_LOW); // Because this is a testing sketch

  Serial.print("Listening on pipe: ");
  Serial.println(pipes[0]);

  radio.openWritingPipe(pipes[1]); // Adress of the Raspberry
  radio.openReadingPipe(1, pipes[0]); // Adress of the Arduino

  radio.startListening();
}

// List of patterns to cycle through.  Each is defined as a separate function below.
typedef void (*SimplePatternList[])();
SimplePatternList gPatterns = { rainbow, rainbowWithGlitter, confetti, sinelon, juggle, bpm };

uint8_t gCurrentPatternNumber = 5; // Index number of which pattern is current
uint8_t gHue = 0; // rotating "base color" used by many of the patterns

void loop()
{
  // Read the settings from the Raspberry
  while (radio.available()) {

    Serial.print("got sth: ");

    char receive_payload[17];

    uint8_t len = radio.getDynamicPayloadSize();

    if (!len) {
      continue;
    }

    radio.read(receive_payload, len);

    receive_payload[len] = 0;

    Serial.println(receive_payload);

    radio.stopListening();
    radio.write(receive_payload, len);
    radio.startListening();

    parsePayload(receive_payload);
  }

  // Call the current pattern function once, updating the 'leds' array
  gPatterns[gCurrentPatternNumber]();

  // send the 'leds' array out to the actual LED strip
  FastLED.show();
  // insert a delay to keep the framerate modest
  FastLED.delay(1000 / fps);

  //Serial.println(gPatternNames[gCurrentPatternNumber]);

  // do some periodic updates
  EVERY_N_MILLISECONDS( hueUpdateDelay ) {
    gHue++;  // slowly cycle the "base color" through the rainbow
  }
  //EVERY_N_SECONDS( 30 ) { nextPattern(); } // change patterns periodically
}

void parsePayload(const String& payload) {
  // Go through all the chars and stop at the '=' char
  String setting = "", valueString = "";
  boolean settingFinished = false;
  for (int i = 0; i < payload.length(); i++) {
    if (payload[i] != '=') {
      if (settingFinished) {
        valueString += payload[i];
      } else {
        setting += payload[i];
      }
    } else {
      settingFinished = true;
    }
  }

  int value = (int) valueString.toInt();

  if (setting.equals("rDH")) {
    rainbowDeltaHue = value;
  } else if (setting.equals("gC")) {
    glitterChance = value;
  } else if (setting.equals("cPU")) {
    confettiPerUpdate = value;
  } else if (setting.equals("cHR")) {
    confettiHueRange = value;
  } else if (setting.equals("sBPM")) {
    sinelonBPM = value;
  } else if (setting.equals("sFS")) {
    sinelonFadeSpeed = value;
  } else if (setting.equals("bBPM")) {
    bpmBPM = value;
  } else if (setting.equals("bHO")) {
    bpmHueOffset = value;
  } else if (setting.equals("bPO")) {
    bpmPartCount = value;
  } else if (setting.equals("bCPI")) {
    bpmColorPaletteIndex = value;
  } else if (setting.equals("jDC")) {
    juggleDotCount = value;
  } else if (setting.equals("jDHI")) {
    juggleDotHueIncrease = value;
  } else if (setting.equals("jFS")) {
    juggleFadeSpeed = value;
  } else if (setting.equals("hUD")) {
    hueUpdateDelay = value;
  } else if (setting.equals("fps")) {
    fps = value;
  } else if (setting.equals("b")) {
    brightness = value;
  } else if (setting.equals("mode")) {
    gCurrentPatternNumber = value;
  }

}

#define ARRAY_SIZE(A) (sizeof(A) / sizeof((A)[0]))

void nextPattern()
{
  // add one to the current pattern number, and wrap around at the end
  gCurrentPatternNumber = (gCurrentPatternNumber + 1) % ARRAY_SIZE(gPatterns);
}

void rainbow()
{
  // FastLED's built-in rainbow generator
  fill_rainbow( leds, NUM_LEDS, gHue, rainbowDeltaHue);
}

void rainbowWithGlitter()
{
  // built-in FastLED rainbow, plus some random sparkly glitter
  rainbow();
  addGlitter(glitterChance);
}

void addGlitter( fract8 chanceOfGlitter)
{
  if ( random8() < chanceOfGlitter) {
    leds[ random16(NUM_LEDS) ] += CRGB::White;
  }
}

void confetti()
{
  // random colored speckles that blink in and fade smoothly
  fadeToBlackBy( leds, NUM_LEDS, 10);
  for (int i = 0; i < confettiPerUpdate; i++) {
    int pos = random16(NUM_LEDS);
    leds[pos] += CHSV( gHue + random8(confettiHueRange), 200, 255);
  }
}

int lastSinelonPosition = 0;

void sinelon()
{
  // a colored dot sweeping back and forth, with fading trails
  fadeToBlackBy( leds, NUM_LEDS, sinelonFadeSpeed);
  int pos = beatsin16( sinelonBPM, 0, NUM_LEDS - 1 );

  int movement = pos - lastSinelonPosition;
  if (movement > 0) {
    for (int i = pos; i < pos + movement + 1; i++) {
      if (i >= 0 && i <= NUM_LEDS - 1) {
        leds[i] += CHSV ( gHue, 255, 192);
      }
    }
  } else {
    for (int i = pos; i > pos + movement - 1; i--) {
      if (i >= 0 && i <= NUM_LEDS - 1) {
        leds[i] += CHSV ( gHue, 255, 192);
      }
    }
  }

  lastSinelonPosition = pos;
}

void bpm()
{
  // colored stripes pulsing at a defined Beats-Per-Minute (BPM)
  uint8_t BeatsPerMinute = bpmBPM;
  CRGBPalette16 palette = colorPalettes[bpmColorPaletteIndex];
  uint8_t beat = beatsin16( BeatsPerMinute, 0, 255);
  for ( int i = 0; i < NUM_LEDS; i++) {
    leds[i] = ColorFromPalette(palette, gHue + (i * bpmHueOffset), beat - gHue + (i * bpmPartCount));
  }
}

void juggle() {
  // eight colored dots, weaving in and out of sync with each other
  fadeToBlackBy( leds, NUM_LEDS, juggleFadeSpeed);
  byte dothue = 0;
  for ( int i = 0; i < juggleDotCount; i++) {
    leds[beatsin16( i + juggleDotCount - 1, 0, NUM_LEDS - 1 )] |= CHSV(dothue, 200, 255);
    dothue += juggleDotHueIncrease;
  }
}
