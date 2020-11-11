# Generated by Django 3.1.1 on 2020-11-11 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name_plural': 'CustomUser'},
        ),
        migrations.AddField(
            model_name='customuser',
            name='age',
            field=models.IntegerField(default=0, verbose_name='年齢'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('male', '男性'), ('female', '女性'), ('NA', 'NA')], default='NA', max_length=6, verbose_name='性別'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='learn_language',
            field=models.CharField(choices=[('ja', '日本語'), ('en', '英語'), ('in', 'インドネシア語')], default='en', max_length=2, verbose_name='学習言語'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='mother_language',
            field=models.CharField(choices=[('ja', '日本語'), ('en', '英語'), ('in', 'インドネシア語')], default='ja', max_length=2, verbose_name='母語'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='nickname',
            field=models.CharField(default='プロフィールを設定してください。', max_length=100, verbose_name='ニックネーム'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='プロフィール写真'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='self_introduction',
            field=models.TextField(blank=True, null=True, verbose_name='自己紹介'),
        ),
    ]
