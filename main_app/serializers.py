from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Contact
from .models import Mapper
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ("name", "email", "phone", "is_spam")


class MapperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mapper
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
