from re import A
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from chat.models import Account



class UserRegistrationForm(UserCreationForm):
	username = forms.CharField(max_length = 255)
	firstname = forms.CharField(max_length = 255)
	lastname = forms.CharField(max_length = 255)
	email = forms.EmailField(max_length = 255)
	date_of_birth = forms.DateField()
	
	class Meta:
		model = Account
		fields = ('username', 'firstname', 'lastname', 'email', 'date_of_birth', 'password1', 'password2')


class EditDetailsForm(UserChangeForm):
	class Meta:
		model = Account
		fields = ('username', 'firstname', 'lastname', 'email', 'date_of_birth', 'password')
		widgets = {
			'username': forms.TextInput(attrs={'class':'form-control'}),
			'firstname': forms.TextInput(attrs={'class':'form-control'}),
			'lastname': forms.TextInput(attrs={'class':'form-control'}),
			'email': forms.TextInput(attrs={'class':'form-control'}),
			'date_of_birth': forms.TextInput(attrs={'class':'form-control'}),
			'password': forms.TextInput(attrs={'class':'form-control'}),
		}



class ChangePasswordForm(PasswordChangeForm):
	old_password = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control'}))
	new_password1 = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control'}))
	new_password2 = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control'}))
	
	class Meta:
		model = Account
		fields = ('old_password', 'new_password1', 'new_password2')
		