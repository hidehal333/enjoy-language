from django import forms
from .models import Comments

class CommentsCreateForm(forms.ModelForm):
    """コメント投稿フォーム"""
    comment_content= forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comments
        fields = ('comment_content', 'photo')
