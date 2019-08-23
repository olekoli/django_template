from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path, reverse_lazy
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from .utils.views import DRFAuthenticatedGraphQLView

router = DefaultRouter()


urlpatterns = [
    path("admin/", admin.site.urls),
    # API
    path("graphql/", DRFAuthenticatedGraphQLView.as_view(graphiql=True)),
    path("v1/", include(router.urls)),
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("api-root"), permanent=False)),
    # Rest Authentication
    path("rest-auth/", include("rest_auth.urls")),
    path("rest-auth/registration/", include("rest_auth.registration.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
