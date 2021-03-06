"""natr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
# from dummy import urls as dummy_urls
from resources import urls as resources_urls



class IndexView(TemplateView):

    template_name = 'index.html'

    def get(self, request, *a, **kw):
        if not request.user.is_anonymous():
            return self.render_to_response(
                self.get_context_data(**kw))
        else:
            return HttpResponseRedirect(reverse('login'))


urlpatterns = [
    url(r'^$', IndexView.as_view(template_name='index.html'), name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^auth/', include('django.contrib.auth.urls'))
]


# urlpatterns += dummy_urls.urlpatterns
urlpatterns += resources_urls.urlpatterns

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
