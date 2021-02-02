from django.test import SimpleTestCase
from django.urls import reverse, resolve

from ..views import signup_view
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView

class TestUrls(SimpleTestCase):

    def test_signup_url(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, signup_view)

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_password_change_url(self):
        url = reverse('password_change')
        self.assertEqual(resolve(url).func.view_class, PasswordChangeView)

    def test_password_change_done_url(self):
        url = reverse('password_change_done')
        self.assertEqual(resolve(url).func.view_class, PasswordChangeDoneView)

    def test_password_reset_url(self):
        url = reverse('password_reset')
        self.assertEqual(resolve(url).func.view_class, PasswordResetView)

    def test_password_reset_done_url(self):
        url = reverse('password_reset_done')
        self.assertEqual(resolve(url).func.view_class, PasswordResetDoneView)

    def test_password_reset_complete_url(self):
        url = reverse('password_reset_complete')
        self.assertEqual(resolve(url).func.view_class, PasswordResetCompleteView)
