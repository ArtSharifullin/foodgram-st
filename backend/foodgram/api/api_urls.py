from django.urls import path
from . import views


urlpatterns = [
    path('quote/', views.get_quote_view, name='weather'),
    path('cat_fact/', views.get_cat_fact_view, name='cat_fact'),
]

urlpatterns += [
    path('run_quote/', views.run_quote_task),
    path('run_cat_fact/', views.run_cat_fact_task),
    path('task_status/<str:task_id>/', views.get_task_status)
]