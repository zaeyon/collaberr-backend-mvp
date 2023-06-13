from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

API_PREFIX = "api/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.apps.home.urls")),
    path(API_PREFIX, include("core.apps.accounts.urls")),
    path(API_PREFIX, include("core.apps.campaigns.urls")),
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

