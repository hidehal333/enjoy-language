from django.urls import path

from . import views

app_name ='pages'
urlpatterns =[
    path('', views.HomePageView.as_view(), name = 'home'),
    path('about/', views.AboutPageView.as_view(), name = 'about'),
    path('inquiry/', views.InquiryPageView.as_view(), name = 'inquiry'),
    path('profile/<int:pk>/', views.listview, name = 'profile'),
    path('profile/update/', views.ProfileChangeView.as_view(), name = 'profile_change'),
    path('user_searcha_all', views.UserSearchAllListView.as_view(), name = 'user_search_all'),
    path('user_search_mother_language', views.UserSearchMLListView.as_view(), name = 'user_search_mother_language'),
    path('user_search_learn_language', views.UserSearchLLListView.as_view(), name = 'user_search_learn_language'),
    path('guest_login/', views.guest_login, name = 'guest_login'),
    path('ajax_usersearchall/', views.ajax_UserSearchAll, name = 'ajax_usersearchall'),
    path('ajax_usersearchlearn/', views.ajax_UserSearchLearn, name = 'ajax_usersearchlearn'),
    path('ajax_usersearchmother/', views.ajax_UserSearchMother, name = 'ajax_usersearchmother'),
    path('user_search/', views.UserSearchPageView.as_view(), name = 'user_search'),
]
