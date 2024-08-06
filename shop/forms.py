from django import forms
from .models import *


class TicketForm(forms.Form):
    
    SUBJECT_CHOICES = (
        ('انتقاد', 'انتقاد'),
        ('پیشنهاد', 'پیشنهاد'),
        ('گزارش', 'گزارش')
    )
    
    message = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=100, required=True)
    phone = forms.CharField(max_length=11)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("شماره تلفن عددی نیست!")
            elif len(phone) > 11:
                raise forms.ValidationError("شماره تلفن اشتباه است!")
            else:
                return phone


class CommentForm(forms.ModelForm):
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            if len(name) < 3:
                raise forms.ValidationError("نام کوتاه است!")
            else:
                return name
        
    def clean_body(self):
        body = self.cleaned_data['body']
        if body:
            if len(body) < 10:
                raise forms.ValidationError("پیام کوتاه است!")
            else:
                return body
    
    class Meta:
        model = Comment
        fields = ['name', 'body']
        


class SearchForm(forms.Form):
    query = forms.CharField()


# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=30, required=True)
#     password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput)


class UserRegister(forms.ModelForm):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput, label="password")
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput, label="repeat password")
    
    class Meta:
        model = User
        fields = ['username', 'email']
        
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("گذرواژه ها مطابقت ندارند!")
        return cd['password']
    
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("این ایمیل قبلا وارد شده!")
        return email
    
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError("این نام کاربری قبلا استفاده شده!")
        return username
    
