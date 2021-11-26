from django import forms
from django.forms import fields
from .models import Account, UserProfile

class RegistrationForms(forms.ModelForm):
    password =forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'form-control'
    }))
    confirm_password =forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password'
    }))
    class Meta: 
        model= Account
        fields =['first_name','last_name','phone_number','email','password']
    
    def clean(self):
        cleaned_data = super(RegistrationForms,self).clean()
        password =cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')


        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match"
            )
    

    def __init__(self,*args,**kwargs):
        super(RegistrationForms,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter First name '
        self.fields['last_name'].widget.attrs['placeholder']='Enter Last name'
        self.fields['phone_number'].widget.attrs['placeholder']='Enter phone number'
        self.fields['email'].widget.attrs['placeholder']='Enter email address'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name','last_name','phone_number')
    
    def __init__(self,*args,**kwargs):
         super(UserForm,self).__init__(*args,**kwargs)
         for field in self.fields:
             self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=('address_line_1','address_line_2','city','state')
    
    def __init__(self,*args,**kwargs):
         super(UserProfileForm,self).__init__(*args,**kwargs)
         for field in self.fields:
             self.fields[field].widget.attrs['class'] = 'form-control'