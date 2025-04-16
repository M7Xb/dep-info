from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('groups/', views.group_list, name='group_list'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/<int:group_id>/edit/', views.edit_group, name='edit_group'),
    path('groups/<int:group_id>/delete/', views.delete_group, name='delete_group'),
    path('users/create/', views.create_user, name='user_create'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    path('settings/', views.site_settings, name='site_settings'),
    path('logs/', views.logs, name='logs'),
    path('announcements/', views.announcement_list, name='announcement_list'),
    path('announcements/<int:id>/', views.announcement_detail, name='announcement_detail'),
    path('api/announcements/<int:pk>/', views.get_announcement, name='get_announcement'),
    path('announcements/create/', views.create_announcement, name='create_announcement'),
    path('announcements/<int:announcement_id>/edit/', views.edit_announcement, name='edit_announcement'),
    path('announcements/<int:announcement_id>/delete/', views.delete_announcement, name='delete_announcement'),
    path('api/announcements/<int:announcement_id>/', views.announcement_detail_api, name='announcement_detail_api'),
    path('ads/', views.ad_list, name='ad_list'),
    path('ads/create/', views.create_ad, name='create_ad'),
    path('ads/<int:ad_id>/edit/', views.edit_ad, name='edit_ad'),
    path('ads/<int:ad_id>/delete/', views.delete_ad, name='delete_ad'),
    path('api/ads/<int:ad_id>/', views.ad_detail_api, name='ad_detail_api'),
    path('timetables/', views.timetable_list, name='timetable_list'),
    path('timetables/upload/', views.upload_timetable, name='upload_timetable'),
    path('timetables/delete/<int:timetable_id>/', views.delete_timetable, name='delete_timetable'),
    path('timetables/<int:timetable_id>/view/', views.view_timetable, name='view_timetable'),
]




























