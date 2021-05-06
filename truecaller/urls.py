from main_app.models import Contact
from django.urls import include, path
from django.contrib import admin
from main_app import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contacts', views.ViewContacts.as_view(), name="view_contacts"),
    path('create_account', views.CreateAccount.as_view(), name="create_account"),
    # path('mark_spam', views.MarkSpam.as_view(), name="mark_spam"),
    # path('contacts', views.Contacts.as_view(), name="contact"),
    path('api-token-auth', obtain_auth_token, name='api_token_auth'),
]