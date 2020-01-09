from django import forms
from .models import Profile

class EditProfileForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3}
        ),
        max_length=250,
        help_text='The max length of the description is 250 characters.')
    
    mode = forms.ChoiceField(choices=((0, "Rainbow"), (1, "Rainbow Glitter"), (2, "Confetti"), (3, "Sinelon"), (4, "Juggle"), (5, "BPM")))

    hueUpdateDelay = forms.IntegerField(label='Hue Update Delay (ms)')
    fps = forms.IntegerField(label='FPS')
    
    rainbowDeltaHue = forms.IntegerField(label='Rainbow|Color Variety')
    
    glitterChance = forms.IntegerField(label='Glitter|Chance Of Glitter Per Update (%)')
    
    confettiPerUpdate = forms.IntegerField(label='Confetti|Confetti Per Update')
    confettiHueRange = forms.IntegerField(label='Confetti Color Variety')
    
    sinelonBPM = forms.IntegerField(label='Sinelon|BPM')
    sinelonFadeSpeed = forms.IntegerField(label='Black Fade Speed')
    bpmBPM = forms.IntegerField(label='BPM|BPM')
    bpmHueOffset = forms.IntegerField(label='Color Variety')
    bpmPartCount = forms.IntegerField(label='Entity Count')
    bpmColorPaletteIndex = forms.ChoiceField(label='Color Palette', choices=((0, "Rainbow"), (1, "Rainbow Stripe"), (2, "Party"), (3, "Heat")))
    juggleDotCount = forms.IntegerField(label='Juggle|Stripe Count')
    juggleDotHueIncrease = forms.IntegerField(label='Stripe Color Difference')
    juggleFadeSpeed = forms.IntegerField(label='Black Fade Speed')

    class Meta:
        model = Profile
        fields = [
            'description',
            'mode',
            'hueUpdateDelay',
            'fps',
            'brightness',
            'rainbowDeltaHue',
            'glitterChance',
            'confettiPerUpdate',
            'confettiHueRange',
            'sinelonBPM',
            'sinelonFadeSpeed',
            'bpmBPM',
            'bpmHueOffset',
            'bpmPartCount',
            'bpmColorPaletteIndex',
            'juggleDotCount',
            'juggleDotHueIncrease',
            'juggleFadeSpeed'
        ]