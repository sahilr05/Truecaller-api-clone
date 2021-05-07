from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token

from main_app import views

schema_view = get_schema_view(
    openapi.Info(
        title="Instahyre Truecaller API's",
        default_version="v1",
        description="Welcome to the world of Jaseci",
        terms_of_service="https://www.jaseci.org",
        contact=openapi.Contact(email="jason@jaseci.org"),
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("contacts", views.ViewContacts.as_view(), name="view_contacts"),
    path(
        "create_account", views.CreateAccount.as_view(), name="create_account"
    ),  # noqa
    path("view_spam", views.ViewSpams.as_view(), name="view_spam"),  # noqa
    path(
        "search_contact", views.SearchContact.as_view(), name="search_contact"
    ),  # noqa
    path("login", obtain_auth_token, name="api_token_auth"),
    path(
        "swagger-ui/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
