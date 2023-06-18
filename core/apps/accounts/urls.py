from rest_framework.routers import SimpleRouter
from django.urls import path
from . import views

router = SimpleRouter()
# api/accounts
router.register('accounts', views.AccountViewSet, basename='accounts')

urlpatterns = [
    # api/login
    path('login/', views.CustomLoginView.as_view(), name='login'),
] + router.urls
