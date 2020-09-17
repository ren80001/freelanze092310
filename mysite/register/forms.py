
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm
)
from django.contrib.auth import get_user_model

User = get_user_model()


class SearchForm(forms.Form):
    title = forms.CharField(
        initial='',
        label='タイトル',
        required = False, # 必須ではない
    )
    text = forms.CharField(
        initial='',
        label='内容',
        required=False,  # 必須ではない
    )

class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる


class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email


class UserUpdateForm(forms.ModelForm):
    """ユーザー情報更新フォーム"""

    top_image = forms.ImageField(widget=forms.FileInput)
    class Meta:
        model = User
        fields = ('nick_name','top_image','twitter','instagram',
                  'skill','area','request_fee','portfolio','self_introduction')#画像はあとで解決する
        widgets = {
            'self_introduction': forms.Textarea(attrs={'cols': 40, 'rows': 10}),
            'portfolio': forms.Textarea(attrs={'cols': 40, 'rows': 10})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


