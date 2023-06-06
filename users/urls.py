from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserView.as_view(), name="user"),
    path('add_user/', views.AddUserView.as_view(), name="add_user"),
    path('', views.LoginView.as_view(), name="login"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('<int:user_id>/', views.UserView.as_view(), name="update_user"),
]
