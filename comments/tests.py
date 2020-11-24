from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from diary.models import Diary
from .models import Comments

class CommentsTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='diaryuser',
            email='diaryuser@email.com',
            password='testpass123'
        )

        self.commentsuser = get_user_model().objects.create_user(
            username='commentsuser',
            email='commentsuser@email.com',
            password='testpass123'
        )

        self.diary = Diary.objects.create(
            user = self.user,
            content='Harry Potter',
        )

        self.comments = Comments.objects.create(
            user = self.commentsuser,
            diary = self.diary,
            comment_content ="good comments"
        )


    def test_comments_listing(self):
        self.assertEqual(f'{self.comments.user}', self.commentsuser.username)
        self.assertEqual(f'{self.comments.comment_content}', 'good comments')

    def test_comment_list_view_for_logged_in_user(self):
        self.client.login(email='diaryuser@email.com', password='testpass123')
        response = self.client.get(reverse('diary:diary_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'good comments')
        self.assertTemplateUsed(response, 'diary/diary_list.html')
