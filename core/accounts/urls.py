from rest_framework.routers import SimpleRouter
from django.urls import path
from . import views

router = SimpleRouter(trailing_slash=False)
router.register('accounts', views.AccountViewSet, basename='accounts')

urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='login'),
] + router.urls

