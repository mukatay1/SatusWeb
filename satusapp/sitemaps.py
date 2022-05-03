from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post


class StaticViewSitemap(Sitemap):
    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)


class PostSitemap(Sitemap):
    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.time_created
