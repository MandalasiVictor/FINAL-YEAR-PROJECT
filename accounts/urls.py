from django.urls import path
from . import views
from accounts.views import CustomPasswordResetView, UserListView, UserUpdateView, UserDeleteView, LoginUserView
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    path('users-index', UserListView.as_view(), name="users-index"),
    path('register-user', views.register_user, name="register-user"),
    path('update-user/<int:pk>/', UserUpdateView.as_view(), name="update-user"),
    path('delete-user/<int:pk>/', UserDeleteView.as_view(), name="delete-user"),
    path('signup/', views.signup_user, name='signup-user'),


    # user authentication
    path('', LoginUserView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'), name='password_reset_request'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name='password_reset_complete'),
    path('reset/', CustomPasswordResetView.as_view(), name='password_reset'),
]