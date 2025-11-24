from django.urls import path
from . import views

urlpatterns = [
    path('run_chuck/', views.run_chuck_joke_task),
    path('run_sw_info/', views.run_SW_info_task),
    path('run_external_batch/', views.run_external_api_batch_task),
    path('run_external_fetch/', views.run_external_api_fetch_task),
    path('task_status/<str:task_id>/', views.get_task_status)
]