from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('post_list/',views.post_list,name='post_list'),
    path('post_list/<str:pk>/',views.post_detail,name='post_details'),
    path('new_post/',views.post_create,name='post_create'),
    path('post_update/<str:pk>',views.post_update,name='post_update'),
    path('post_delete/<str:pk>',views.post_delete,name='post_delete'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('signup/',views.signup_user,name='signup'),
    path('comment_delete/<str:pk>',views.comment_delete,name='comment_delete'),
    path('profile/<str:pk>',views.author_profile,name='author_profile')
]