from django import forms
from .models import Server
from user.models import User


class CreateServerForm(forms.ModelForm):
    name = forms.CharField(max_length=25, required=True, label='Enter Name')
    description = forms.CharField(max_length=200, widget=forms.TextInput, label='Enter Description')

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