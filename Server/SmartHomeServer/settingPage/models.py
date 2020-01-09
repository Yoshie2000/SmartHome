# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    name = models.CharField(max_length=30, unique=True, default='New profile')
    description = models.CharField(max_length=250, default='Description')
    # settings
    mode = models.IntegerField(default=0)
    hueUpdateDelay = models.IntegerField(default=10)
    fps = models.IntegerField(default=120)
    brightness = models.IntegerField(default=80)
    
    rainbowDeltaHue = models.IntegerField(default=1)
    
    glitterChance = models.IntegerField(default=75)
    
    confettiPerUpdate = models.IntegerField(default=1)
    confettiHueRange = models.IntegerField(default=16)
    
    sinelonBPM = models.IntegerField(default=80)
    sinelonFadeSpeed = models.IntegerField(default=10)
    
    bpmBPM = models.IntegerField(default=100)
    bpmHueOffset = models.IntegerField(default=1)
    bpmPartCount = models.IntegerField(default=10)
    bpmColorPaletteIndex = models.IntegerField(default=0)
    
    juggleDotCount = models.IntegerField(default=4)
    juggleDotHueIncrease = models.IntegerField(default=64)
    juggleFadeSpeed = models.IntegerField(default=10)
    
    def setting_codes(self):
        return "mode=" + str(self.mode) + ";hUD=" + str(self.hueUpdateDelay) + ";fps=" + str(self.fps) + ";b=" + str(self.brightness) + ";rDH=" + str(self.rainbowDeltaHue) + ";gC=" + str(self.glitterChance) + ";cPU=" + str(self.confettiPerUpdate) + ";cHR=" + str(self.confettiHueRange) + ";sBPM=" + str(self.sinelonBPM) + ";sFS=" + str(self.sinelonFadeSpeed) + ";bBPM=" + str(self.bpmBPM) + ";bHO=" + str(self.bpmHueOffset) + ";bPC=" + str(self.bpmPartCount) + ";bCPI=" + str(self.bpmColorPaletteIndex) + ";jDC=" + str(self.juggleDotCount) + ";jDHI=" + str(self.juggleDotHueIncrease) + ";jFS=" + str(self.juggleFadeSpeed)
    
    def __str__(self):
        return self.name