from django import forms
from .models import Server
from user.models import User


class CreateServerForm(forms.ModelForm):
    name = forms.CharField(max_length=25, required=True, label='Server Name')
    description = forms.CharField(max_length=200, widget=forms.TextInput, label='Server Description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')

        if name:
            name = name.title()
    
        return cleaned_data
    
    def save(self, username):
        server = super().save(commit=True)
        if username:
            user = User.objects.get(username=username)
            server.set_owner(user)
        return server

    class Meta:
        model = Server
        fields = ["name", "description"]

class SearchServerForm(forms.Form):
    name = forms.CharField(max_length=25, required=True, label="Search Name")
    owner = forms.CharField(max_length=25, required=False, label="Owner Filter")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].widget.attrs.update({
            'Placeholder': 'Optional'
        })
    
