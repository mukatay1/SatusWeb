from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from satusapp.sitemaps import StaticViewSitemap, PostSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'post': PostSitemap
}

urlpatterns = [
    path('satus_admin/', admin.site.urls),
    path('', include('satusapp.urls')),
    path('accounts/', include('allauth.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),

]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
