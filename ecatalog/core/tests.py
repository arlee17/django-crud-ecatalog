from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm

class CoreTests(TestCase):
    def setUp(self):
        self.signup_url = reverse('core:signup')
        self.login_url = reverse('core:login')
        self.logout_url = reverse('core:logout')
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        
    def test_signup(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/signup.html')
        self.assertIsInstance(response.context['form'], SignUpForm)
        response = self.client.post(self.signup_url, data=self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:login'))
        
        user = User.objects.get(username=self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password1']))
        
        
    def test_login(self):        
        response = self.client.post(self.login_url, data={
            'username': self.user_data['username'],
            'password': self.user_data['password1']
        })
        
        response = self.client.post(self.login_url, data={
            'username': self.user_data['username'],
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        
        
    def test_logout(self):
        self.client.login(username=self.user_data['username'], password=self.user_data['password1'])

        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:index'))
        