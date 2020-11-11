from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""

    LANGUAGE = (
            ('ja', _('日本語')),
            ('en', _('英語')),
            ('in', _('インドネシア語')),
        )

    GENDER = (
            ('male', _('男性')),
            ('female', _('女性')),
            ('NA', 'NA'),
    )

    nickname = models.CharField(verbose_name=_('ニックネーム'), max_length=100, default=_('プロフィールを設定してください。'))
    mother_language = models.CharField(verbose_name=_('母語'),max_length=2, choices=LANGUAGE, default = 'ja')
    learn_language = models.CharField(verbose_name=_('学習言語'), max_length=2, choices=LANGUAGE, default = 'en')
    gender = models.CharField(verbose_name=_('性別'),max_length=6, choices=GENDER, default = 'NA')
    age = models.IntegerField(verbose_name=_('年齢'), default=0)
    self_introduction = models.TextField(verbose_name=_('自己紹介'), blank=True, null=True)
    profile_photo = models.ImageField(verbose_name=_('プロフィール写真'), blank=True, null=True)

    class Meta:
        verbose_name_plural = 'CustomUser'
