from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

API_PREFIX = "api/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(API_PREFIX, include("core.accounts.urls")),
    path(API_PREFIX, include("core.campaigns.urls")),
    # path("", include("core.apps.home.urls")),
    # path("creator/", include("core.apps.creator.urls")),
    # path("business/", include("core.apps.business.urls")),
    # path("campaign/", include("core.apps.campaign.urls")),
    # path("accounts/", include("core.apps.user.urls")),
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
