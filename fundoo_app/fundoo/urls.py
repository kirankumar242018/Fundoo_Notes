from django.urls import path, include, re_path
from django.conf.urls import url

from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # rest api url
    # path('', views.UserListView.as_view()),

    # test this one
    path('dash_board1/', views.dash_board1, name='dash_board1'),
    path('index/', views.index, name='index'),

    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', views.logout, name='logout'),
    path('user_profile/', views.user_profile, name='user_profile'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate,
        name='activate'),


    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='fundoo/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='fundoo/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='fundoo/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='fundoo/password_reset_complete.html'
         ),
         name='password_reset_complete'),



    # notes urls
    path('home/', views.home, name='home'),
    path('home1/', views.home1, name='home1'),

    path('notevisual/', views.home1, name='home1'),

    #  *****Note CRUD Operations***
    path('createnote/', views.createnote, name='createnote'),
    path('deletenote/<int:pk>', views.deletenote, name='deletenote'),

    path('copynote/<int:pk>', views.copynote, name='copynote'),
    path('restore/<int:pk>', views.restore, name='restore'),
    #  *****Note Normal Operations***
    path('setcolor/', views.setcolor, name='setcolor'),
    path('ispinned/', views.ispinned, name='ispinned'),
    path('isarchive/', views.isarchive, name='isarchive'),

    path('show_archive/', views.show_archive, name='show_archive'),
    path('show_trash/', views.show_trash, name='show_trash'),


    # ****Label CRUD Operations *****
    path('create_label/', views.create_label, name='create_label'),


























    # url(r'^photo/(?P<photo_id>[0-9]+)/$', views.photo, name='photourl')

    # re_path(r'([0-9]+)/favorite/', views.favorite, name='favorite'),

    #  registration reset password,conformation...

    # url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]