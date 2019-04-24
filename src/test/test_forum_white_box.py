from django.contrib.auth.models import User
from django.test import TestCase, Client
from account.models import ExpertAccount
from forum.models import Topic, Answer


class ForumURLTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create client for test
        cls.client = Client()
        cls.user_1 = User.objects.create(username='test_user', first_name='test', last_name='user')
        cls.user_profile_1 = ExpertAccount.objects.create(user=cls.user_1)

        # create object of it
        cls.topic_1 = Topic.objects.create(author=cls.user_1, title='abc')
        cls.answer_1 = Answer.objects.create(topic=cls.topic_1, author=cls.user_1)

    def test_topic_creation_case_1(self):
        self.assertEqual(self.topic_1.__str__(), 'abc')

    def test_topic_creation_case_2(self):
        self.topic_2 = Topic.objects.create(author=self.user_1, title='abc')
        self.assertNotEqual(self.topic_2.slug, 'abc')
        self.topic_2.delete()

    def test_answer_creation_case(self):
        self.assertEqual(self.answer_1.__str__(), 'On: abc by test user')
