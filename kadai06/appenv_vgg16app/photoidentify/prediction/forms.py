from django import forms  # type: ignore

class ImageUploadForm(forms.Form):
    image = forms.ImageField()