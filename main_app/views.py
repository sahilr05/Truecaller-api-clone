from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Contact
from .models import Mapper
from .models import Profile
from .serializers import ContactSerializer
from .serializers import ProfileSerializer
from .serializers import UserSerializer


# Authenticate by passing username and password to /login
# A token would be obtained.. pass that token in header .. for example
# curl -X "GET" "http://127.0.0.1:8000/view_users" -H 'Authorization: Token <obtained_token_here>'


class ViewContacts(APIView):
    permission_classes = (IsAuthenticated,)

    # retrieve all contacts from Profiles and Saved contacts of registered users
    def get(self, request):
        response = []

        queryset_users = User.objects.all().order_by("username")
        queryset_profiles = [
            Profile.objects.filter(user=profile_user) for profile_user in queryset_users
        ]
        for profile in queryset_profiles:
            response.append(ProfileSerializer(profile.first()).data)

        queryset_contacts = Contact.objects.all().order_by("name")
        contacts_serializer = ContactSerializer(queryset_contacts, many=True)
        response.append(contacts_serializer.data)

        return Response(response)

    # add contact in users' phonebook
    @csrf_exempt
    def post(self, request):
        data = request.data
        new_contact = Contact.objects.create(
            name=data["name"], phone=data["phone"]
        )  # noqa
        Mapper.objects.create(user=request.user, contact=new_contact)
        return Response({"200": "OK"}, status=status.HTTP_200_OK)


# create account
class CreateAccount(APIView):
    @csrf_exempt
    def post(self, request):
        data = request.data

        # throws 409 conflict error if existing username detected
        if (data["username"],) in User.objects.values_list("username"):
            return Response(
                {"409": "Conflict", "duplicate error": "user already exists"},
                status=status.HTTP_409_CONFLICT,
            )

        # throws 409 conflict error if existing phone number detected
        if (data["phone"],) in Profile.objects.values_list("phone"):
            return Response(
                {"409": "Conflict", "duplicate error": "number already exists"},  # noqa
                status=status.HTTP_409_CONFLICT,
            )

        AccountSerializer = UserSerializer(
            data={
                "username": data["username"],
                "email": data["email"],
                "password": data["password"],
            }
        )

        if AccountSerializer.is_valid():
            AccountSerializer.save()

        Profile.objects.create(user=User.objects.last(), phone=data["phone"])

        return JsonResponse(
            {
                "phone": str(Profile.objects.last().phone),
                "user": str(User.objects.last().username),
            }
        )


class ViewSpams(APIView):
    permission_classes = (IsAuthenticated,)

    # retrieves spam numbers from contact book of registered users but not registered users
    def get(self, request):
        SpamNumbers = Contact.objects.filter(is_spam=True)
        serializer = ContactSerializer(SpamNumbers, many=True)
        return Response(serializer.data)

    # marks number as spam. Number can be registered or unregistered
    @csrf_exempt
    def put(self, request):
        contact_serializer = None
        profile_serializer = None

        phone = request.data["phone"]
        if (phone,) in Contact.objects.values_list("phone"):
            get_number_from_contacts = Contact.objects.get(phone=phone)
            contact_serializer = ContactSerializer(
                get_number_from_contacts, data={"is_spam": True}, partial=True
            )
        if (phone,) in Profile.objects.values_list("phone"):
            get_number_from_profile = Profile.objects.get(phone=phone)
            profile_serializer = ProfileSerializer(
                get_number_from_profile, data={"is_spam": True}, partial=True
            )

        if contact_serializer and contact_serializer.is_valid():
            contact_serializer.save()
        if profile_serializer and profile_serializer.is_valid():
            profile_serializer.save()

        return Response({"200": "OK"}, status=status.HTTP_200_OK)


class SearchContact(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        response = []

        param = request.GET.get("name") or request.GET.get("phone")

        # if search query contains name then goes into the following function
        if param and param.isalpha():

            search_name = request.GET["name"]

            # if any contact name starts with searched name
            contact_prefix = Contact.objects.filter(name__startswith=search_name)
            if contact_prefix:
                for contact in contact_prefix:
                    response.append(ContactSerializer(contact).data)

            # if name of registered user starts with searched name
            profile_user_prefix = User.objects.filter(username__startswith=search_name)
            if profile_user_prefix:
                profile_prefix = [
                    Profile.objects.filter(user=profile_user)
                    for profile_user in profile_user_prefix
                ]
                for profile in profile_prefix:
                    response.append(ProfileSerializer(profile.first()).data)

            # rest of the numbers not matching with searched query
            if response:
                not_in_contacts = Contact.objects.all().exclude(
                    name__startswith=search_name
                )
                profiles = User.objects.all().exclude(username__startswith=search_name)
                not_in_profile = [
                    Profile.objects.filter(user=profile_user)
                    for profile_user in profiles
                ]

                for contact in not_in_contacts:
                    response.append(ContactSerializer(contact).data)
                for contact in not_in_profile:
                    if contact:
                        response.append(ProfileSerializer(contact.first()).data)

                return Response(response)

            # contact name containing searched name
            in_contacts = Contact.objects.filter(name__contains=search_name)
            if in_contacts:
                for contact in in_contacts:
                    response.append(ContactSerializer(contact).data)

            # name of registered user containing searched name
            profile_user = User.objects.filter(username__contains=search_name)
            if profile_user:
                in_profile = Profile.objects.filter(user=profile_user.first())
                for contact in in_profile:
                    response.append(ProfileSerializer(contact.first()).data)

            # rest of the contacts not containing searched name
            not_in_contacts = Contact.objects.all().exclude(name=search_name)
            profiles = User.objects.all().exclude(username=search_name)
            not_in_profile = [
                Profile.objects.filter(user=profile_user) for profile_user in profiles
            ]

            for contact in not_in_contacts:
                response.append(ContactSerializer(contact).data)
            for contact in not_in_profile:
                if contact:
                    response.append(ProfileSerializer(contact.first()).data)

            return Response(response)

        # if searched parameter is a phone number
        elif param and param.isdigit():
            search_phone = request.GET["phone"]

            # check if entered phone number is registered user
            registered_user = Profile.objects.filter(phone=search_phone)

            # return if registered user
            if registered_user:
                response.append(ProfileSerializer(registered_user.first()).data)
                return Response(response)

            # check if entered number is in contact book of any other registered user
            unregistered_user = Contact.objects.filter(phone=search_phone)
            for contact in unregistered_user:
                response.append(ContactSerializer(contact).data)

        # if param is empty
        else:
            queryset = Contact.objects.all().order_by("name")
            serializer = ContactSerializer(queryset, many=True)
            return Response(serializer.data)

        return Response(response)
