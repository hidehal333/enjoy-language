from django.urls import path

from . import views

app_name ='comments'
urlpatterns =[
    path('creat/<int:pk>/', views.CommentsCreateView.as_view(), name = 'comments_create'),
    path('delete/<int:pk>/', views.CommentsDeleteView.as_view(), name = 'comments_delete'),
]
