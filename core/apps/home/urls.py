from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, HomeView

app_name = "home"
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('change_password/', auth_views.PasswordChangeView.as_view(), name="password_change"),
    path('change_password/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    ]
