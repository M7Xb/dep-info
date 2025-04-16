from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import home_view, timetables_view, view_timetable_public

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('admin_dashboard.urls')),
    path('', home_view, name='home'),
    path('timetables/', timetables_view, name='timetables'),
    path('timetables/<int:timetable_id>/view/', view_timetable_public, name='view_timetable'),
    path('dashboard/users/api/<int:user_id>/', views.user_detail_api, name='user_detail_api'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





