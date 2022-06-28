from django.urls import path
from . import views 
urlpatterns = [
    path('', views.index),
    path('pred',views.home,name='home'),
    path('forum',views.forum,name='forum'),
    path('post',views.postquery,name='postquery')
]
