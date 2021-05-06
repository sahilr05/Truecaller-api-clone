from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email" ,"password")

class AddPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("phone","is_spam")



# class EditMemeSerializer(serializers.ModelSerializer):
#     def validate(self, data):
#         url = data["url"]
#         mimetype, encoding = mimetypes.guess_type(url)
#         if not mimetype:
#             raise serializers.ValidationError(({"url": "Invalid url !!"}))
#         return data

#     class Meta:
#         model = UploadMeme
#         fields = ("caption", "url")