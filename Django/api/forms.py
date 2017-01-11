# coding=utf-8
from django import forms
from django.contrib.auth.models import User

# Register your models here.
ALLOW_CHAR = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


class EditUserForm(forms.Form):
    username = forms.CharField(label=u"昵称", max_length=40)
    # email_new=forms.EmailField(label=u'新邮件',max_length=40)
    password_new = forms.CharField(label=u"新密码", max_length=20)

    def clean_email(self):
        #验证重复email

        emails=User.objects.filter(email__exact=self.cleaned_data['email_new'])
        if len(emails)<=1:
            return self.cleaned_data["email_new"]
        raise forms.ValidationError(u"该邮箱已经被使用请使用其他的邮箱")


    def clean_password(self):
        if len(self.cleaned_data['password_new']) < 6:
            raise forms.ValidationError(u"密码长度不能小于6")
        if len(self.cleaned_data['password_new']) > 10:
            raise forms.ValidationError(u"密码长度不能大于10")
        else:
            for a in self.cleaned_data['password_new']:
                if a not in ALLOW_CHAR:
                    raise forms.ValidationError(u"密码仅能用字母或数字")
        return self.cleaned_data['password_new']

    def clean(self):
        """验证其他非法"""
        cleaned_data = super(EditUserForm, self).clean()

        if cleaned_data.get("password") == cleaned_data.get("username"):
            raise forms.ValidationError(u"用户名和密码不能一样")
        if cleaned_data.get("password_new") == cleaned_data.get("password_old"):
            raise forms.ValidationError(u"新旧密码相同")
        # if cleaned_data.get("password_new") == cleaned_data.get("password_new_2"):
        #    raise forms.ValidationError(u"新输入的两次密码不一致")
        return cleaned_data


