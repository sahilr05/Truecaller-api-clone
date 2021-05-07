from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from main_app import views

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
]
