"""agrisync URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include
from django.conf import settings
from django.views.generic import RedirectView
from adminsettings.admin import adminsettings

admin.site.index_title = settings.INDEX_TITLE
admin.site.site_title = settings.SITE_TITLE
admin.site.site_header = settings.SITE_HEADER

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    url(r'^login/$', LoginView.as_view(template_name='forum/login.html',
                                       redirect_authenticated_user=True), name='login'),
    url(r'^logout/$', LogoutView.as_view(next_page='login'), name='logout'),
    url(r'^favicon.ico$', favicon_view),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/settings/', adminsettings.urls),
    url(r'^account/', include('oauth.urls', namespace='account'), kwargs={'MAINTENANCE': 'OAUTH_APP_MAINTENANCE'}),
    url(r'^forum/', include('forum.urls', namespace='forum'), kwargs={'MAINTENANCE': 'FORUM_APP_MAINTENANCE'}),
    url(r'^', include('main.urls', namespace='main'), kwargs={'MAINTENANCE': 'MAIN_APP_MAINTENANCE'}),
]

if settings.DEBUG:  # pragma: no cover
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
