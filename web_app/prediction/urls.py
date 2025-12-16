from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('check-symptoms/', views.predict_view, name='predict'),
    path('about/', views.about_view, name='about'),
    path('chat/', views.chat_view, name='chat'),
    # Specific paths must come before the generic chat_id pattern
    path('chat/new/', views.new_chat_view, name='new_chat'),
    path('chat/delete/', views.delete_chat_view, name='delete_current_chat'),
    path('chat/delete/<str:chat_id>/', views.delete_chat_view, name='delete_chat'),
    # Generic pattern captures everything else
    path('chat/<str:chat_id>/', views.chat_view, name='chat_with_id'),
    path('set-api-key/', views.set_api_key, name='set_api_key'),
    path('check-allergy-remedies/', views.check_allergy_remedies, name='check_allergy_remedies'),
]
