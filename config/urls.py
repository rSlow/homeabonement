from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path("", include("apps.urls")),

    path("admin/", admin.site.urls),
    path("docs/", include("django.contrib.admindocs.urls")),

    path("accounts/", include("allauth.urls")),

    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
