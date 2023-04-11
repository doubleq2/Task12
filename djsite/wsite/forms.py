from django import forms
from wsite.models import Photo


class ImageForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('title', 'image', 'user')