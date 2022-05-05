from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.template.defaultfilters import slugify as django_slugify
from django.db import models

# Create your models here.
User = get_user_model()

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


def slugify(s):
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))


class Post(models.Model):
    name = models.CharField(max_length=1000)
    context = models.TextField(max_length=1000)
    time_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
    photo = models.ManyToManyField('MultipleImages', blank=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Post'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name[0:25] + str(self.author))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'satus_slug': self.slug})

    def __str__(self):
        return self.name


class MultipleImages(models.Model):
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)


class UserProfile(models.Model):
    GENDER = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('none', 'None')

    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    bio = models.CharField(max_length=50, blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, default='photos/2022/04/06/profile_man.jpg')
    gender = models.CharField(max_length=6, choices=GENDER, default='none')
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    phone = models.BigIntegerField(null=True, blank=True)
    city = models.CharField(max_length=30)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.user))
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfile'


class Comment(models.Model):
    context = models.TextField(max_length=50)
    time_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-time_created')

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comment'


class Thread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    class Meta:
        verbose_name = 'Thread'
        verbose_name_plural = 'Thread'


class Message(models.Model):
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE, related_name="thread", blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    body = models.CharField(max_length=1000)
    time_created = models.DateTimeField(default=timezone.now)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.body + ' ' + str(self.time_created.date())

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Message'


class Notification(models.Model):
    notification_type = models.PositiveSmallIntegerField()
    to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_from')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    created_time = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notification'

