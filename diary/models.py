from django.utils.translation import gettext_lazy as _

from users.models import CustomUser
from django.db import models


class Diary(models.Model):
    """日記モデル"""

    user = models.ForeignKey(CustomUser, verbose_name=_('ユーザー'), on_delete=models.PROTECT)
    content = models.TextField(verbose_name=_('本文'))
    photo1 = models.ImageField(verbose_name=_('写真1'), blank=True, null=True)
    photo2 = models.ImageField(verbose_name=_('写真2'), blank=True, null=True)
    photo3 = models.ImageField(verbose_name=_('写真3'), blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('作成日時'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('更新日時'), auto_now=True)
    like = models.ManyToManyField(CustomUser, related_name='like', blank=True)

    class Meta:
        verbose_name_plural = 'Diary'

    def __str__(self):
        return self.title
