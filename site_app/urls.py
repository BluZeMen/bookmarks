from django.conf.urls import url, include
from django.contrib import admin
from registration.forms import RegistrationFormUniqueEmail
from registration.backends.hmac.views import RegistrationView


urlpatterns = [
    url(r'^accounts/register/$', RegistrationView.as_view(), {'form': RegistrationFormUniqueEmail},
        name='registration_register'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('bookmarks.urls'), name='bookmarks'),

]
