from .models import User, Post
from .forms import PostForm
from django.test import TestCase
from django.urls import reverse


class PostTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='ExampleUser', password='ExampleUserPassword123')
        self.post = Post.objects.create(name='ExamplePostName1', context='ExamplePostContext1',
                                        author=self.user)
        self.form = PostForm()

    def test_post_list(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'satusapp/index.html')

    def test_post_detail(self):
        response = self.client.get(reverse('detail', kwargs={'satus_slug': self.post.slug}))
        self.assertEquals(response.status_code, 200)

    def test_post_create(self):
        data = {
            'name': 'ExamplePostName',
            'context': 'ExamplePostContext',
            'author': self.user

        }
        response = self.client.post(reverse('home'), data)
        self.assertEquals(response.status_code, 200)

    def test_post_update(self):
        self.client.login(username='ExampleUser', password='ExampleUserPassword123')
        data = {
            'name': 'ExamplePostName[CHANGED]',
            'context': 'ExamplePostContext',
            'author': self.user
        }
        response = self.client.put(reverse('update', kwargs={'satus_slug': self.post.slug}), data)
        self.assertEquals(response.status_code, 200)

    def test_post_name_label(self):
        field_label = self.post._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_post_form(self):
        self.assertEquals(self.form.fields.get('name').label, 'Титул')
