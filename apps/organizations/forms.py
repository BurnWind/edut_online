__author__ = 'wzy'
__date__ = '2020/2/26 16:06'

import re

from django import forms

from operation.models import UserConsole

class UserConsoleForm(forms.ModelForm):

    class Meta:
        model = UserConsole
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        '''
        验证手机号码是否合法
        :return:
        '''
        mobile = self.cleaned_data['mobile']
        REGEX_PHONE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_PHONE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码不合法', code='invalid_mobile')

