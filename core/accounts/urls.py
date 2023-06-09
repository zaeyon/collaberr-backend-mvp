from rest_framework.routers import SimpleRouter
from django.urls import path
from . import views


app_name = "accounts"

router = SimpleRouter(trailing_slash=False)
router.register('accounts', views.AccountViewSet, basename='accounts')

urlpatterns = router.urls
