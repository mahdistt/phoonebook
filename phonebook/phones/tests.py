from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.urls import reverse


class MyPhonebookViewTest(TestCase):
    """
        tests phone book :
    """

    def setUp(self) -> None:
        pass

    def test_auth_required(self):
        response = self.client.get(reverse('phones:show_all_number'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/phones/login/?', response.url)
        response = self.client.get(reverse('phones:show_all_number'), follow=True)
        self.assertContains(response, 'Username:')

    def test_login_and_empty_phonebook(self):
        user = get_user_model().objects.create(username='user1')
        self.client.force_login(user=user)
        response = self.client.get(reverse('phones:show_all_number'))
        self.assertContains(response, 'Last')
        # self.assertEqual(response.context_data['paginator'].count, 0)
        # paginator nemidonam chetori bayad select konam


class MyPhonebookSearchTest(TestCase):
    """
        tests phone book :
    """

    def setUp(self) -> None:
        pass

    def test_auth_required(self):
        response = self.client.get(reverse('phones:search'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/phones/login/?', response.url)
        response = self.client.get(reverse('phones:search'), follow=True)
        self.assertContains(response, 'Username:')

    def test_login_and_search_form(self):
        user = get_user_model().objects.create(username='user1')
        self.client.force_login(user=user)
        response = self.client.get(reverse('phones:search'))
        self.assertContains(response, 'Enter phone number:')


class AddNumberTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_auth_required(self):
        response = self.client.get(reverse('phones:show-add-entry-form'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/phones/login/?', response.url)
        response = self.client.get(reverse('phones:show-add-entry-form'), follow=True)
        self.assertContains(response, 'Username:')

    def test_login_and_add_form(self):
        user = get_user_model().objects.create(username='user1')
        self.client.force_login(user=user)
        response = self.client.get(reverse('phones:show-add-entry-form'))
        self.assertContains(response, 'Name:')


class MyBioTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_auth_required(self):
        response = self.client.get(reverse('phones:edit-profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/phones/login/?', response.url)
        response = self.client.get(reverse('phones:edit-phone'), follow=True)
        self.assertContains(response, 'Username:')

    def test_login_and_add_form(self):
        user = get_user_model().objects.create(username='user1')
        self.client.force_login(user=user)
        response = self.client.get(reverse('phones:edit-profile'))
        self.assertContains(response, 'First name:')
