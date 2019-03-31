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
    url(r'^login/$', LoginView.as_view(template_name='oauth/login.html',
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
