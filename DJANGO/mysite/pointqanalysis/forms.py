from django import forms

def validate_file_extension(value):
    if not value.name.endswith('.txt'):
        raise forms.ValidationError(u'Error: Wrong file extension')
        
class Form_upload_fil (forms.Form):
    name = forms.CharField(max_length=100)
    simul_txt_db = forms.FileField(validators=[validate_file_extension])