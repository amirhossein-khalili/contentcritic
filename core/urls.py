from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls", namespace="accounts")),
    path("api/notifications/", include("notification.urls", namespace="notification")),
    path("api/content/", include("content.urls", namespace="content")),
]
