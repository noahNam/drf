from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from ..models import *
from ..serializers import *

"""
    python manage.py test --settings=drf_project.settings.local

    python manage.py test
        django project 전체에서 tests*.py
"""

# Create your tests here.
class PostViewTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        print(self.user)

        self.post = Post.objects.create(author=self.user, title="test title", content="test_content")
        print(self.post)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_authorization_enforced(self):
        new_client = APIClient()
        res = new_client.get('/post/viewset/post/', format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_can_create_a_post(self):
        post_data = {
            "title": "create test",
            "content": "create content",
            "author": 1
        }

        res = self.client.post('/post/viewset/post/', post_data, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_post_list(self):
        res = self.client.get('/post/viewset/post/', format='json')

        posts = Post.objects.all()
        serializers = PostSerializer(posts, many=True)

        self.assertEqual(res.data['result'], serializers.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
