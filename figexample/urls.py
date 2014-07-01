from django.conf.urls import patterns, include, url
from rest_framework import routers
from django.contrib import admin
from .views import UserViewSet, GroupViewSet, EmployeeViewSet  # employee_list, employee_detail


admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'employees', EmployeeViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'figexample.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/v1/', include(router.urls)),
    # url(r'^employees/$', employee_list, name='employee-list'),
    # url(r'^employees/(?P<pk>[0-9]+)$', employee_detail, name='employee-detail'),
    url(r'^api-auth', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^admin/', include(admin.site.urls)),
)
