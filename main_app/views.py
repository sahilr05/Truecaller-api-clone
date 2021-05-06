from functools import partial
from django.shortcuts import render, resolve_url

from django.contrib.auth.models import User
from .models import Contact, Profile
from django.http import JsonResponse
from .serializers import CreateAccountSerializer, AddPhoneSerializer
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class ViewUsers(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        queryset = User.objects.values("id")
        return Response(queryset)

class CreateAccount(APIView):
    @csrf_exempt
    def post(self, request):
        data = request.data

        if (data['username'],) in User.objects.values_list('username'):
            return JsonResponse({"duplicate error": "User already exists"})

        AccountSerializer = CreateAccountSerializer(data= \
                            {'username':data['username'], \
                            'email':data['email'], \
                            'password': data['password']}
                        )
        if AccountSerializer.is_valid():
            AccountSerializer.save()

        PhoneSerializer = AddPhoneSerializer(data={'phone':data['phone']})

        if PhoneSerializer.is_valid():
            PhoneSerializer.save()

        AddedNumber = Profile.objects.last()
        AddedNumber.user = User.objects.last()   
        AddedNumber.save()     

        return JsonResponse({"phone": str(Profile.objects.last().phone), \
                            'user': str(User.objects.last().username)})

class MarkSpam(APIView):
    permission_classes = (IsAuthenticated,)

    @csrf_exempt
    def post(self, request):
        data = request.data
        MarkSpam = data['is_spam']

        try:
            Number = get_object_or_404(Profile, phone=data['phone'])
            PhoneSerializer = AddPhoneSerializer(Number, data={'is_spam':MarkSpam}, partial=True)
        except Exception as E:
            PhoneSerializer = AddPhoneSerializer(data={'phone':data['phone'], 'is_spam': MarkSpam})

        if PhoneSerializer.is_valid():
            PhoneSerializer.save()

        return JsonResponse({"phone":data['phone'], "is_spam":MarkSpam})

class Contacts(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        User = request.user.profile_set.first()
        ContactList = User.user_contacts.values_list('contact_name')
        return Response(ContactList)

    @csrf_exempt
    def post(self, request):
        data = request.data
        Name = data['name']
        PhoneNumber = data['phone']

        NewContact = Contact.objects.create(contact_name=Name)

        UserProfile = request.user.profile_set.first()
        ExistingContacts = UserProfile.user_contacts.all()

        ExistingNumbers = []
        for Contact in ExistingContacts:
            ExistingNumbers.append(Contact.profile.first().phone)

        if PhoneNumber in ExistingNumbers:
            return Response(f"{PhoneNumber} already exists in your phone book")

        if (PhoneNumber,) in Profile.objects.values_list('phone'):
            SelectedNumber = Profile.objects.get(phone=PhoneNumber)
            NewContact.profile.add(SelectedNumber)
        else:
            NewProfile = Profile.objects.create(phone=PhoneNumber)
            NewContact.profile.add(NewProfile)

        return Response(f"Added {PhoneNumber} in your contact book")
        


        # if pk:
        #     upload_meme = get_object_or_404(UploadMeme, pk=pk)
        #     serializer = EditMemeSerializer(upload_meme, data=request.data)
        # else:
        #     upload_meme = None
        #     serializer = UploadMemeSerializer(data=request.data)
        # if not serializer.is_valid():
        #     return Response({"serializer": serializer, "upload_meme": upload_meme})

        # serializer.save()
        # return redirect("meme_app:view_memes")
    