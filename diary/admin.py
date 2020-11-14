from django.contrib import admin

from .models import Diary
from comments.models import Comments


class CommentsInline(admin.TabularInline):
    model = Comments

class DiaryAdmin(admin.ModelAdmin):
    inlines = [
        CommentsInline,
    ]
    list_display = ('content', 'user', 'created_at')
    ordering = ('-created_at',)

admin.site.register(Diary, DiaryAdmin)
