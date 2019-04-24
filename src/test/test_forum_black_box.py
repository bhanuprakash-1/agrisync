from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from account.models import ExpertAccount
from forum.models import Topic, Answer


class ForumURLWithoutLogInTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create client for test
        cls.client = Client()
        cls.user_1 = User.objects.create(username='test_user', first_name='test', last_name='user')
        cls.user_profile_1 = ExpertAccount.objects.create(user=cls.user_1)

        # create object of it
        cls.topic_1 = Topic.objects.create(author=cls.user_1, title='abc')
        cls.answer_1 = Answer.objects.create(topic=cls.topic_1, author=cls.user_1)

    def test_forum_urls_without_login_case_1(self):
        # without login --> redirect to login page
        response = self.client.get(reverse('forum:index'))
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('forum:index'))

    def test_forum_urls_without_login_case_2(self):
        response = self.client.get(reverse('forum:answered-by-user'))
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('forum:answered-by-user'))

    def test_forum_urls_without_login_case_3(self):
        response = self.client.get(reverse('forum:add_topic'))
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('forum:add_topic'))

    def test_forum_urls_without_login_case_4(self):
        response = self.client.get(self.topic_1.get_absolute_url())
        self.assertRedirects(response, reverse('login') + "?next=" + self.topic_1.get_absolute_url())

    def test_forum_urls_without_login_case_(self):
        response = self.client.get(self.topic_1.get_edit_url())
        self.assertRedirects(response, reverse('login') + "?next=" + self.topic_1.get_edit_url())

    def test_forum_urls_without_login_case_6(self):
        response = self.client.get(self.topic_1.get_delete_url())
        self.assertRedirects(response, reverse('login') + "?next=" + self.topic_1.get_delete_url())

    def test_forum_urls_without_login_case_7(self):
        response = self.client.get(self.answer_1.get_delete_url())
        self.assertRedirects(response, reverse('login') + "?next=" + self.answer_1.get_delete_url())


class ForumURLWithoutPermissionTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create client for test
        cls.client = Client()
        cls.user_1 = User.objects.create(username='test_user', first_name='test', last_name='user')
        cls.user_profile_1 = ExpertAccount.objects.create(user=cls.user_1)

        # create object of it
        cls.topic_1 = Topic.objects.create(author=cls.user_1, title='abc')
        cls.answer_1 = Answer.objects.create(topic=cls.topic_1, author=cls.user_1)

        # login from different account
        cls.user_2 = User.objects.create(username='test_user_2', first_name='test', last_name='user')

    def test_forum_urls_without_permission_case_1(self):
        self.client.force_login(user=self.user_2)
        response = self.client.get(reverse('forum:index'))
        self.assertEqual(response.status_code, 200)

    def test_forum_urls_without_permission_case_2(self):
        self.client.force_login(user=self.user_2)
        response = self.client.get(reverse('forum:answered-by-user'))
        self.assertEqual(response.status_code, 200)

    def test_forum_urls_without_permission_case_3(self):
        self.client.force_login(user=self.user_2)
        response = self.client.get(self.topic_1.get_edit_url())
        self.assertEqual(response.status_code, 403)


class ForumURLWithPermissionTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create client for test
        cls.client = Client()
        cls.user_1 = User.objects.create(username='test_user', first_name='test', last_name='user')
        cls.user_profile_1 = ExpertAccount.objects.create(user=cls.user_1)

        # create object of it
        cls.topic_1 = Topic.objects.create(author=cls.user_1, title='abc')

    def test_forum_urls_with_permission_case_1(self):
        self.client.force_login(user=self.user_1)
        response = self.client.get(reverse('forum:index') + '?q=test')
        self.assertEqual(response.status_code, 200)

    def test_forum_urls_with_permission_case_2(self):
        self.client.force_login(user=self.user_1)
        response = self.client.get(reverse('forum:index') + '?q=test')
        self.assertTemplateUsed(response, 'forum/index.html')

    def test_forum_urls_with_permission_case_3(self):
        self.client.force_login(user=self.user_1)
        response = self.client.get(reverse('forum:index') + '?q=')
        self.assertEqual(response.status_code, 200)

    def test_forum_urls_with_permission_case_4(self):
        self.client.force_login(user=self.user_1)
        response = self.client.get(reverse('forum:index') + '?q=')
        self.assertTemplateUsed(response, 'forum/index.html')

    def test_forum_urls_with_permission_case_5(self):
        self.client.force_login(user=self.user_1)
        data = {'title': 'abcd', 'content': 'abcd', 'tags': 'ab,cd', 'category': 'Q'}
        response = self.client.post(reverse('forum:add_topic'), data, follow=True)
        self.assertRedirects(response, reverse('forum:detail', kwargs={'slug': 'abcd'}))

    def test_forum_urls_with_permission_case_6(self):
        self.client.force_login(user=self.user_1)
        data = {'topic': self.topic_1.id, 'author': self.user_1.id, 'content': '&nbsp;'}
        response = self.client.post(self.topic_1.get_absolute_url(), data)
        self.assertEqual(response.status_code, 200)

    def test_forum_urls_with_permission_case_7(self):
        self.client.force_login(user=self.user_1)
        data = {'topic': self.topic_1.id, 'author': self.user_1.id, 'content': '   '}
        self.client.post(self.topic_1.get_absolute_url(), data)
        self.assertFalse(Answer.objects.filter(author=self.user_1).count())

    def test_forum_urls_with_permission_case_8(self):
        self.client.force_login(user=self.user_1)
        data = {'topic': self.topic_1.id, 'author': self.user_1.id, 'content': 'abcde'}
        response = self.client.post(self.topic_1.get_absolute_url(), data, follow=True)
        self.assertRedirects(response, self.topic_1.get_absolute_url())

    def test_forum_urls_with_permission_case_9(self):
        self.client.force_login(user=self.user_1)
        data = {'topic': self.topic_1.id, 'author': self.user_1.id, 'content': 'abcde'}
        self.client.post(self.topic_1.get_absolute_url(), data, follow=True)
        self.assertEqual(Answer.objects.filter(author=self.user_1).count(), 1)

    def test_forum_urls_without_login_case_10(self):
        self.client.force_login(user=self.user_1)
        response = self.client.get(self.topic_1.get_delete_url())
        self.assertEqual(response.status_code, 404)

    def test_forum_urls_without_login_case_11(self):
        self.client.force_login(user=self.user_1)
        self.answer_1 = Answer.objects.create(topic=self.topic_1, author=self.user_1)
        response = self.client.get(reverse('forum:delete_answer', kwargs={'pk': self.answer_1.pk}))
        self.assertEqual(response.status_code, 404)

    def test_forum_urls_without_login_case_12(self):
        self.client.force_login(user=self.user_1)
        self.answer_1 = Answer.objects.create(topic=self.topic_1, author=self.user_1)
        response = self.client.post(reverse('forum:delete_answer', kwargs={'pk': self.answer_1.pk}))
        self.assertEqual(response.status_code, 302)

    def test_forum_urls_without_login_case_13(self):
        self.client.force_login(user=self.user_1)
        self.answer_1 = Answer.objects.create(topic=self.topic_1, author=self.user_1)
        self.client.post(reverse('forum:delete_answer', kwargs={'pk': self.answer_1.pk}))
        self.assertFalse(Answer.objects.filter(topic=self.topic_1).exists())

