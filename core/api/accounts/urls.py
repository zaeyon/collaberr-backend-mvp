from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import AccountViewSet, CustomLoginView, LogoutView

router = SimpleRouter()
# api/accounts/
router.register(r'accounts', AccountViewSet, basename='accounts')

urlpatterns = [
    # api/login/
    path('login/', CustomLoginView.as_view(), name='login'),
    # api/logout/
    path('logout/', LogoutView.as_view(), name='logout'),
]

urlpatterns += router.urls
