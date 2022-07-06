from django.urls import path
from . import views 
urlpatterns = [
    path('index', views.index,name='index'),
    path('pred',views.home,name='home'),
    path('forum',views.forum,name='forum'),
    path('post',views.postquery,name='postquery'),
    path('',views.signin,name='login'),
    path('register',views.signup,name='register'),
    path('answer/<int:id>',views.answerpage,name='answers')
]
