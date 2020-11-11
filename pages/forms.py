from django import forms
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser

#お問い合わせページ
class InquiryForm(forms.Form):
    name = forms.CharField(label=_('お名前'), max_length=30)
    email = forms.EmailField(label=_('メールアドレス'))
    title = forms.CharField(label=_('タイトル'), max_length=30)
    message = forms.CharField(label=_('メッセージ'), widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control col-9'
        self.fields['name'].widget.attrs['placeholder'] =_( 'お名前をここに入力してください。')

        self.fields['email'].widget.attrs['class'] = 'form-control col-11'
        self.fields['email'].widget.attrs['placeholder'] = _('メールアドレスをここに入力してください。')

        self.fields['title'].widget.attrs['class'] = 'form-control col-11'
        self.fields['title'].widget.attrs['placeholder'] = _('タイトルをここに入力してください。')

        self.fields['message'].widget.attrs['class'] = 'form-control col-12'
        self.fields['message'].widget.attrs['placeholder'] = _('メッセージをここに入力してください。')

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message= self.cleaned_data['message']

        subject = 'お問い合わせ {}'.format(title)
        message = '送信者名: {0}\nメールアドレス: {1}\nメッセージ: {2}'.format(name, email, message)
        from_email ='admin@example.com'
        to_list =[
            'test@example.com'
        ]
        cc_list =[
            email
        ]

        message =EmailMessage(subject = subject, body=message, from_email = from_email, to = to_list, cc = cc_list)
        message.send()

#プロフィール編集用
class ProfileChangeForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ( 'profile_photo', 'nickname', 'gender','age', 'mother_language', 'learn_language', 'self_introduction')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def update(self, user):
        user.profile_photo = self.cleaned_data['profile_photo']
        user.nickname = self.cleaned_data['nickname']
        user.gender = self.cleaned_data['gender']
        user.age = self.cleaned_data['age']
        user.mother_language = self.cleaned_data['mother_language']
        user.learn_language = self.cleaned_data['learn_language']
        user.self_introduction = self.cleaned_data['self_introduction']
        user.save()
