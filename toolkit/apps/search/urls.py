from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^search_filters/$', views.SearchFilterList.as_view(), name="search_filters_list_api"),
    url(r'^search_filters/(?P<pk>[0-9]+)/$', views.SearchFilterDetail.as_view(), name="search_filters_detail_api"),
    # url(r'^users/$', views.UserList.as_view(), name="users_list_api"),
    # url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name="users_detail_api"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
