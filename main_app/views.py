from functools import partial
from django.shortcuts import render, resolve_url

from django.contrib.auth.models import User
from .models import Contact, Profile
from django.http import JsonResponse
from .serializers import *
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class ViewContacts(APIView):
    def get(self, request):
        queryset = Contact.objects.all().order_by('name')
        serializer = ContactSerializer(queryset, many=True)
        return Response(serializer.data)

    permission_classes = (IsAuthenticated,)

    @csrf_exempt
    def post(self, request):
        data = request.data
        new_contact = Contact.objects.create(name=data['name'], phone=data['phone'])
        Mapper.objects.create(user = request.user, contact = new_contact)
        return Response({"200": "OK"}, status=status.HTTP_200_OK)

class CreateAccount(APIView):
    @csrf_exempt
    def post(self, request):
        data = request.data

        if (data['username'],) in User.objects.values_list('username'):
            return Response({"409": "Conflict", "duplicate error":"user already exists"}, status=status.HTTP_409_CONFLICT)
            
        AccountSerializer = UserSerializer(data= \
                            {'username':data['username'], \
                            'email':data['email'], \
                            'password': data['password']}
                        )
        if AccountSerializer.is_valid():
            AccountSerializer.save()

        Profile.objects.create(user=User.objects.last(), phone=data['phone'] )

        return JsonResponse({"phone": str(Profile.objects.last().phone), \
                            'user': str(User.objects.last().username)})

class ViewSpams(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        SpamNumbers = Contact.objects.filter(is_spam=True)
        serializer = ContactSerializer(SpamNumbers, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def put(self, request):
        contact_serializer=None
        profile_serializer=None

        phone = request.data['phone']
        if (phone,) in Contact.objects.values_list('phone'):
            get_number_from_contacts = Contact.objects.get(phone=phone)
            contact_serializer = ContactSerializer(get_number_from_contacts, data={'is_spam':True}, partial=True)
        if (phone,) in Profile.objects.values_list('phone'):
            get_number_from_profile = Profile.objects.get(phone=phone)
            profile_serializer = ProfileSerializer(get_number_from_profile, data={'is_spam':True}, partial=True)

        if contact_serializer and contact_serializer.is_valid():
            contact_serializer.save()
        if  profile_serializer and profile_serializer.is_valid():
            profile_serializer.save()

        return Response({"200": "OK"}, status=status.HTTP_200_OK)
    
class SearchContact(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        response = []

        param = request.GET.get('name') or request.GET.get('phone')

        if param and param.isalpha():
            search_name = request.GET['name']       
            in_contacts = Contact.objects.filter(name=search_name)

            for contact in in_contacts:
                response.append(ContactSerializer(contact).data)

            not_in_contacts = Contact.objects.all().exclude(name=search_name)

            for contact in not_in_contacts:
                response.append(ContactSerializer(contact).data)

        elif param and param.isdigit():
            search_phone = request.GET['phone']       
            in_contacts = Contact.objects.filter(phone=search_phone).exclude(email__exact='')

            if in_contacts:
                response.append(ContactSerializer(in_contacts.first()).data)
                return Response(response)
                # for contact in in_contacts:
                #     response.append(ContactSerializer(contact).data)

            not_in_contacts = Contact.objects.filter(phone=search_phone)
            for contact in not_in_contacts:
                response.append(ContactSerializer(contact).data)
        else:
            queryset = Contact.objects.all().order_by('name')
            serializer = ContactSerializer(queryset, many=True)
            return Response(serializer.data)

        return Response(response)

