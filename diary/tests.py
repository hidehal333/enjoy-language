from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from diary.models import Diary

class DiaryTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='diaryuser',
            email='diaryuser@email.com',
            password='testpass123'
        )

        self.diary = Diary.objects.create(
            user = self.user,
            content='Harry Potter',
        )


    def test_dialy_listing(self):
        self.assertEqual(f'{self.diary.user}', self.user.username)
        self.assertEqual(f'{self.diary.content}', 'Harry Potter')

    def test_dialy_list_view_for_logged_in_user(self):
        self.client.login(email='diaryuser@email.com', password='testpass123')
        response = self.client.get(reverse('diary:diary_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'diary/diary_list.html')

    def test_diary_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('diary:diary_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '%s?next=/diary/list/' % (reverse('account_login')))
        response = self.client.get(
            '%s?next=/diary/list/' % (reverse('account_login')))
        self.assertContains(response, 'Log In')
