from django.urls import path
from .views import *
urlpatterns = [
    path('tasks/', tasks, name='tasks'),  # This will now handle task details
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('register/login/', login),
    path('doodle/', doodle, name='doodle'),
    path('home/', home, name='home'),
    path('logout/', logout, name='logout'),
    path('task/<int:task_id>/pending/', mark_as_pending, name='mark_as_pending'),
    path('task/<int:task_id>/completed/', mark_as_completed, name='mark_as_completed'),
    path('task/<int:task_id>/delete_task/', delete_task, name='delete_task'),
    path('draw',doodle,name='draw'),
    path('statistics/', statistics, name='statistics'),
]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)