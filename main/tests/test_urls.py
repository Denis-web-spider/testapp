from django.test import SimpleTestCase
from django.urls import reverse, resolve

from ..views import tests_view, test_detail_view, testing_view

class TestUrls(SimpleTestCase):

    def test_testing_url(self):
        url = reverse('testing', args=[1, 1])
        self.assertEqual(resolve(url).func, testing_view)

    def test_test_detail_url(self):
        url = reverse('test_detail', args=[1])
        self.assertEqual(resolve(url).func, test_detail_view)

    def test_tests_url(self):
        url = reverse('tests')
        self.assertEqual(resolve(url).func, tests_view)
