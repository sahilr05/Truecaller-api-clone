from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.fields import EmailField
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phone = models.CharField(
        validators=[phone_regex], max_length=15, blank  =False, unique=True
    )
    # contacts = models.ForeignKey(User, null=True, related_name='user_contacts', on_delete=models.CASCADE)
    is_spam = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.phone}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length = 254)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone = models.CharField(
        validators=[phone_regex], max_length=15, blank=False
    )
    is_spam = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
class Mapper(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='user_contacts')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}"
    

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


# class GlobalUsers(models.Model):
#     name = models.CharField(unique=True, max_length=100)
#     phone = PhoneNumberField(null=False, blank=False, unique=True)
#     email = models.EmailField()
#     contacts = models.ForeignKey(User, related_name='user_contacts', on_delete=models.CASCADE)
#     is_spam = models.BooleanField(default=False)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return f"{self.name}"