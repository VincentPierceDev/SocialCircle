from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='', max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True, label='', max_length=50)
    password2 = forms.CharField(widget=forms.PasswordInput, label='', required=True, max_length=50)
    agree_to_terms = forms.BooleanField(help_text='I agree to all Terms and Conditions', label='', required=True)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_error_msg()
        self.setup_attribs()

    def setup_error_msg(self):
        self.fields['password1'].error_messages = {
            'required': 'Please Enter A Password',
            'max_length': 'Password Must Be Less Than 50 Characters',
        }

        self.fields['password2'].error_messages = {
            'required': 'Please Re-Enter Your Password',
            'max-length': 'Password Confirmation Must Be Less Than 50 Characters'
        }

    def setup_attribs(self):
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email',
            'class': 'form-field'
        })

        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'form-field'
        })

        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password',
            'class': 'form-field'
        })

        self.fields['agree_to_terms'].widget.attrs.update({
            'class': 'check-field'
        })

    def clean(self):
        clean_data = super().clean()
        return clean_data

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password fields did not match")

    def clean_email(self):
        data = self.cleaned_data.get('email')
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("The provided email is already registered")
        return data

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'agree_to_terms']

class AccountSetupForm(forms.ModelForm):
    username = forms.CharField(required=True, max_length=25, label='')
    bio = forms.CharField(required=False, max_length=250, widget=forms.TextInput, label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_error_messages()
        self.setup_attribs()

    def setup_error_messages(self):
        self.fields['username'].error_messages = {
            'required': "Please Provide A Username",
            'max_length': "Username is too long, must be shorter than 25 characters"
        }

        self.fields['bio'].error_messages = {
            'max_length': "Bio is too long, must be shorter than 250 characters"
        }
        return
    
    def setup_attribs(self):
        self.fields['username'].widget.attrs.update({
            'Placeholder': 'UserName',
            'class': 'form-field'
        });
        self.fields['bio'].widget.attrs.update({
            'Placeholder': 'Write A Bio...',
            'class': 'form-field',
            'id': 'bio-field'
        })
        return

    def clean(self):
        clean_data = super().clean()
        self.clean_username()
        return clean_data
    
    def clean_username(self):
        name = self.cleaned_data.get('username')
        if User.objects.filter(username=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("The username is already taken")
        return name;

    class Meta:
        model = User
        fields = ['username', 'bio']

class AccountLoginForm(AuthenticationForm):
    username = forms.CharField(required=True, label='')
    password = forms.CharField(required=True, label='', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_attributes()
        self.setup_error_messages()

    def setup_attributes(self):
        self.fields["username"].widget.attrs.update({
            'placeholder': 'Username',
            'class': 'form-field'
        })

        self.fields["password"].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'form-field'
        })

    def setup_error_messages(self):
        self.fields['username'].error_messages = {
            'required': 'Please provide a username.',
            'invalid_login': 'Please enter a correct username and password.'
        }

        self.fields['password'].error_messages = {
            'required': 'Please provide a password.',
            'invalid_login': 'Please enter a correct username and password.'
        }