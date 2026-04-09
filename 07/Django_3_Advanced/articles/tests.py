from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Article, UserFavouriteArticle

class TestPrivateViewsAccess(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.article = Article.objects.create(
            title='Test Article',
            author=self.user,
            synopsis='Test synopsis',
            content='Test content'
        )

    def test_favourites_requires_login(self):
        response = self.client.get(reverse('favourites'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/login/?next=/en/favourites/'))

        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('favourites'))
        self.assertEqual(response.status_code, 200)

    def test_publications_requires_login(self):
        response = self.client.get(reverse('publications'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('publications'))
        self.assertEqual(response.status_code, 200)

    def test_publish_requires_login(self):
        response = self.client.get(reverse('publish'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('publish'))
        self.assertEqual(response.status_code, 200)

class TestRegisterViewAccess(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_register_allowed_for_anonymous(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_denied_for_registered(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('register'))
        self.assertIn(response.status_code, [302, 403])

class TestFavouriteDuplicates(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.article = Article.objects.create(
            title='Test Article',
            author=self.user,
            synopsis='Test synopsis',
            content='Test content'
        )

    def test_cannot_add_same_favourite_twice(self):
        self.client.login(username='testuser', password='password123')

        response = self.client.post(reverse('add_favourite'), {'article': self.article.id})
        self.assertEqual(UserFavouriteArticle.objects.filter(user=self.user, article=self.article).count(), 1)
        
        response = self.client.post(reverse('add_favourite'), {'article': self.article.id})

        self.assertEqual(UserFavouriteArticle.objects.filter(user=self.user, article=self.article).count(), 1)
