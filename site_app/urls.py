from django.conf.urls import url, include
from django.contrib import admin
import django.contrib.auth.views as auth_views
# from registration.backends.hmac.views import RegistrationView


urlpatterns = [
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'common/login.html'}),
    # url(r'^accounts/register/$', RegistrationView.as_view(), {'form': RegistrationFormUniqueEmail},
    # name='registration_register'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('bookmarks.urls')),

]
