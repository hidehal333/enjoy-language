from django.utils.translation import gettext_lazy as _
from users.models import CustomUser
from diary.models import Diary
from django.db import models


class Comments(models.Model):
    """コメントモデル"""

    user = models.ForeignKey(CustomUser, verbose_name=_('ユーザー'), on_delete=models.PROTECT)
    diary = models.ForeignKey(Diary, verbose_name=_('日記'), on_delete=models.CASCADE)
    comment_content = models.CharField(verbose_name=_('コメント'), max_length=400)
    photo = models.ImageField(verbose_name=_('写真'), blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('作成日時'), auto_now_add=True)


    class Meta:
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.comment_content
