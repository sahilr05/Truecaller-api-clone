from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class MapperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mapper
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

