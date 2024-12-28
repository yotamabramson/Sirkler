from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),         # Welcome page
    path('register/', views.register_page, name='register'),  # Registration
    path('login/', views.login_page, name='login'),  # Login page
    path('home/', views.home, name='home'),          # Home for logged-in users
    path('logout/', views.logout_view, name='logout'),
    path('circle/<int:circle_id>/', views.circle_detail, name='circle_detail'),
    path('create-circle/', views.create_circle, name='create_circle'),

]

