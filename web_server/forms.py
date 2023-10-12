from django import forms

class UploadFileForm(forms.Form):
    bucket_name = forms.CharField(max_length=10)
    file_name = forms.CharField(max_length=50)
    file = forms.FileField()