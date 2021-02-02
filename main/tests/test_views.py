from django.test import TestCase, Client
from django.urls import reverse, resolve
from ..models import Tests, Questions, Answers
from django.contrib.auth import get_user_model

class TestViews(TestCase):

    def setUp(self):

        self.client = Client()

        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@email.com',
            phone_number='+380674278265',
            password='secret'
        )

        self.test = Tests.objects.create(
            test_name='Simple test',
            test_text='Simple test text'
        )

        self.question_1 = Questions.objects.create(
            question_text='Question text_1',
            test=self.test
        )

        self.question_2 = Questions.objects.create(
            question_text='Question text_2',
            test=self.test
        )

        self.answer_1 = Answers.objects.create(
            answer_text='Answer text_1',
            votes=0,
            question=self.question_1
        )

        self.answer_2 = Answers.objects.create(
            answer_text='Answer text_2',
            votes=0,
            question=self.question_2
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_tests_view(self):

        # user is not authenticated
        response = self.client.get(reverse('tests'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).url_name, 'login')

        logged_in = self.client.login(username=self.user.username, password='secret')
        response = self.client.get(reverse('tests'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tests.html')
        self.assertContains(response, self.test.test_name)

    def test_test_detail_view(self):

        # user is not authenticated
        response = self.client.get(reverse('test_detail', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).url_name, 'login')

        # user is authenticated
        logged_in = self.client.login(username=self.user.username, password='secret')
        response = self.client.get(reverse('test_detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'test_detail.html')
        self.assertContains(response, self.test.test_name)
        self.assertContains(response, self.test.test_text)

        response = self.client.get(reverse('test_detail', args=[2]))
        self.assertEqual(response.status_code, 404)

    def test_testing_view(self):

        # user is not authenticated
        response = self.client.get(reverse('testing', args=[1, 1]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).url_name, 'login')

        # inconsistent answer
        # user is authenticated
        logged_in = self.client.login(username=self.user.username, password='secret')
        response = self.client.get(reverse('testing', args=[1, 2]))
        self.assertEqual(response.status_code, 404)

        # consistent answer
        response = self.client.get(reverse('testing', args=[1, 1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'testing.html')
        self.assertContains(response, self.question_1.question_text)
        self.assertContains(response, self.answer_1.answer_text)

        # consistent answer without answer
        response = self.client.post(reverse('testing', args=[1, 2]), {'current_question': 2})
        self.assertEqual(response.status_code, 404)

        response = self.client.post(reverse('testing', args=[1, 2]), {'current_question': 2, 'answer': self.answer_1.pk})
        self.assertEqual(response.status_code, 200)
        # vote is detected
        self.assertEqual(Answers.objects.filter(pk=self.answer_1.pk)[0].votes, 1)
        self.assertTemplateUsed(response, 'testing.html')
        self.assertContains(response, self.question_2.question_text)
        self.assertContains(response, self.answer_2.answer_text)

        # last question page
        response = self.client.post(reverse('testing', args=[1, 3]), {'current_question': 3, 'answer': self.answer_2.pk, 'last_question': 'True'})
        self.assertEqual(response.status_code, 200)
        # vote is detected
        self.assertEqual(Answers.objects.filter(pk=self.answer_2.pk)[0].votes, 1)
        self.assertTemplateUsed(response, 'finish_test.html')
