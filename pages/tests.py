from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, Client, TestCase
from django.urls import reverse, resolve
from . import views


from diary.models import Diary

#home(トップページ)
class HomepageTests(SimpleTestCase):


    def setUp(self):
        url = reverse('pages:home')
        self.response = self.client.get(url)


    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)


    def test_homepage_url_name(self):
        self.assertEqual(self.response.status_code, 200)


    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'home.html')


    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, '言語を楽しもう！')


    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')

    def test_homepage_url_resolves_homepageview(self):
        view = resolve('/')
        self.assertEqual(
            view.func.__name__,
            views.HomePageView.as_view().__name__
        )

#Aboutページ
class AboutPageTests(SimpleTestCase):


    def setUp(self):
        url = reverse('pages:about')
        self.response = self.client.get(url)


    def test_aboutpage_status_code(self):
        self.assertEqual(self.response.status_code, 200)


    def test_aboutpage_template(self):
        self.assertTemplateUsed(self.response, 'about.html')


    def test_aboutpage_contains_correct_html(self):
        self.assertContains(self.response, 'About | Enjoy Language')


    def test_aboutpage_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')


    def test_aboutpage_url_resolves_aboutpageview(self):
        view = resolve('/about/')
        self.assertEqual(
            view.func.__name__,
            views.AboutPageView.as_view().__name__
        )

#お問い合わせページ
class InquiryPageTests(SimpleTestCase):


    def setUp(self):
        url = reverse('pages:inquiry')
        self.response = self.client.get(url)


    def test_aboutpage_status_code(self):
        self.assertEqual(self.response.status_code, 200)


    def test_aboutpage_template(self):
        self.assertTemplateUsed(self.response, 'inquiry.html')


    def test_aboutpage_contains_correct_html(self):
        self.assertContains(self.response, 'お問い合わせ')


    def test_aboutpage_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')


    def test_aboutpage_url_resolves_aboutpageview(self):
        view = resolve('/inquiry/')
        self.assertEqual(
            view.func.__name__,
            views.InquiryPageView.as_view().__name__
        )

#プロフィールページ


class ProfilePageTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='diaryuser',
            email='diaryuser@email.com',
            password='testpass123',
            nickname  = 'will',
            age = '33'
        )

        self.diary = Diary.objects.create(
            user = self.user,
            content='Harry Potter',
        )


    def test_profile_listing(self):
        self.assertEqual(f'{self.user.username}',  'diaryuser')
        self.assertEqual(f'{self.user.email}', 'diaryuser@email.com')
        self.assertEqual(f'{self.user.nickname}', 'will')
        self.assertEqual(f'{self.user.age}', '33')

    def test_profile_view_for_logged_in_user(self):
        self.client.login(email='diaryuser@email.com', password='testpass123')
        response = self.client.get(self.user.get_absolute_url())
        #no_response = self.client.get('/profile/12345/')
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'will')
        self.assertTemplateUsed(response, 'profile.html')
