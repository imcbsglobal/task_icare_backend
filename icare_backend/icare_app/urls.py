from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', views.register_visitor, name='register_visitor'),
    path('api/admin-login/', views.admin_login, name='admin_login'),
    path('api/dashboard/', views.dashboard_data, name='dashboard_data'),
    
    # Showcase endpoints
    path('api/showcase/', views.showcase_list_create, name='showcase_list_create'),
    path('api/showcase/<int:pk>/', views.showcase_detail, name='showcase_detail'),
    
    # Demonstration endpoints
    path('api/demonstration/', views.demonstration_list_create, name='demonstration_list_create'),
    path('api/demonstration/<int:pk>/', views.demonstration_detail, name='demonstration_detail'),
]