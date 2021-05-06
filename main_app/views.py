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
        queryset = Contact.objects.all()
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
    
    @csrf_exempt
    def put(self, request):
        phone = request.data['phone']
        if (phone,) in Contact.objects.values_list('phone'):
            get_number_from_contacts = get_object_or_404(Contact, phone=phone)
            contact_serializer = ContactSerializer(get_number_from_contacts, data={'is_spam':True}, partial=True)
        if (phone,) in Contact.objects.values_list('phone'):
            get_number_from_profile = get_object_or_404(Profile, phone=phone)
            profile_serializer = ProfileSerializer(get_number_from_profile, data={'is_spam':True}, partial=True)

        if contact_serializer.is_valid():
            contact_serializer.save()
        if  profile_serializer.is_valid():
            profile_serializer.save()
            
        return Response({"200": "OK"}, status=status.HTTP_200_OK)
    

# class MarkSpam(APIView):
#     permission_classes = (IsAuthenticated,)

#     @csrf_exempt
#     def post(self, request):
#         data = request.data
#         MarkSpam = data['is_spam']

#         try:
#             Number = get_object_or_404(Profile, phone=data['phone'])
#             PhoneSerializer = AddPhoneSerializer(Number, data={'is_spam':MarkSpam}, partial=True)
#         except Exception as E:
#             PhoneSerializer = AddPhoneSerializer(data={'phone':data['phone'], 'is_spam': MarkSpam})

#         if PhoneSerializer.is_valid():
#             PhoneSerializer.save()

#         return JsonResponse({"phone":data['phone'], "is_spam":MarkSpam})

# class Contacts(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         User = request.user.profile_set.first()
#         ContactList = User.user_contacts.values_list('contact_name')
#         return Response(ContactList)

#     @csrf_exempt
#     def post(self, request):
#         data = request.data
#         Name = data['name']
#         PhoneNumber = data['phone']

#         NewContact = Contact.objects.create(contact_name=Name)

#         UserProfile = request.user.profile_set.first()
#         ExistingContacts = UserProfile.user_contacts.all()

#         ExistingNumbers = []
#         for Contact in ExistingContacts:
#             ExistingNumbers.append(Contact.profile.first().phone)

#         if PhoneNumber in ExistingNumbers:
#             return Response(f"{PhoneNumber} already exists in your phone book")

#         if (PhoneNumber,) in Profile.objects.values_list('phone'):
#             SelectedNumber = Profile.objects.get(phone=PhoneNumber)
#             NewContact.profile.add(SelectedNumber)
#         else:
#             NewProfile = Profile.objects.create(phone=PhoneNumber)
#             NewContact.profile.add(NewProfile)

#         return Response(f"Added {PhoneNumber} in your contact book")
        


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
    