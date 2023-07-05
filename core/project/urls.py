from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

API_PREFIX = "api/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(API_PREFIX, include("core.api.accounts.urls")),
    path(API_PREFIX, include("core.api.campaigns.urls")),
    path(API_PREFIX, include("core.api.authentications.urls")),
    path(API_PREFIX, include("core.api.creators.urls")),
    path(API_PREFIX, include("core.api.youtube_analytics.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
