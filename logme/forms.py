from django import forms
from django.contrib.auth import forms as user_forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm

class RegistrationForm(user_forms.UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2', 'email']

    def clean_first_name(self):
        return self.cleaned_data['first_name'].capitalize()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].capitalize()

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1', '')
        if len(password1) < 6:
            raise forms.ValidationError("Password must be at least 6 characters.")
        return password1
        
    def clean_password2(self):
        password2 = self.cleaned_data.get('password2', '')
        if len(password2) < 6:
            raise forms.ValidationError("Password must be at least 6 characters.")
        return password2

 
class PasswordChangeForm(user_forms.SetPasswordForm):    
    
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': ("Your old password was entered incorrectly. "
                                "Please enter it again."),
                                })

    old_password = forms.CharField(label="Old password",
                                   widget=forms.PasswordInput)

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
                )
        return old_password
   
    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1', '')
        if len(new_password1) < 6:
            raise forms.ValidationError("Password must be at least 6 characters.")
        return new_password1
        
    def clean_new_password2(self):
        new_password2 = self.cleaned_data.get('new_password2', '')
        if len(new_password2) < 6:
            raise forms.ValidationError("Password must be at least 6 characters.")
        return new_password2