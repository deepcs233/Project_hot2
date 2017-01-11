# coding=utf-8
from django import forms
from django.contrib.auth.models import User

# Register your models here.
ALLOW_CHAR = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


class RegisterForm(forms.Form):
    username = forms.CharField(label=u"昵称", max_length=40,
                               widget=forms.TextInput(attrs={'size': 40, 'class': "form-control"}))
    email = forms.EmailField(label=u"邮件", max_length=40,
                             widget=forms.EmailInput(attrs={'size': 40, 'class': "form-control"}))
    password = forms.CharField(label=u"密码", max_length=20,
                               widget=forms.PasswordInput(attrs={'size': 20, 'class': "form-control"}))

    # re_password=forms.CharField(label=u"重复密码",max_length=20,
    #        widget=forms.PasswordInput(attrs={'size': 20,'class':"form-control"}))

    def clean_username(self):
        '''验证昵称'''
        if len(self.cleaned_data["username"]) < 4:
            raise forms.ValidationError(u"昵称长度不能小于4")
        else:
            for a in self.cleaned_data["username"]:
                if a not in ALLOW_CHAR:
                    raise forms.ValidationError(u"昵称仅能用字母或数字")

        users = User.objects.filter(username__iexact=self.cleaned_data["username"])
        if not users:
            return self.cleaned_data["username"]
        else:
            raise forms.ValidationError(u"该昵称已经被使用请使用其他的昵称")

    def clean_email(self):
        '''验证重复email'''
        emails = User.objects.filter(email__iexact=self.cleaned_data["email"]).filter(is_active=True)
        if not emails:
            return self.cleaned_data["email"]
        raise forms.ValidationError(u"该邮箱已经被使用请使用其他的邮箱")

    def clean_password(self):
        if len(self.cleaned_data["password"]) < 6:
            raise forms.ValidationError(u"密码长度不能小于6")
        else:
            for a in self.cleaned_data["password"]:
                if a not in ALLOW_CHAR:
                    raise forms.ValidationError(u"密码仅能用字母或数字")
        return self.cleaned_data["password"]

    def clean(self):
        """验证其他非法"""
        cleaned_data = super(RegisterForm, self).clean()

        if cleaned_data.get("password") == cleaned_data.get("username"):
            raise forms.ValidationError(u"用户名和密码不能一样")
        # if cleaned_data.get("password") != cleaned_data.get("re_password"):
        #    raise forms.ValidationError(u"两次输入密码不一致")

        return cleaned_data



