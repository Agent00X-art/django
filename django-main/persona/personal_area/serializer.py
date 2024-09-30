from rest_framework import serializers

from .models import PersonalData, Message

class PersonalDataSerializer(serializers.Serializer): # сериалайзер для персональных данных

    Surname = serializers.CharField(max_length=20)
    Name = serializers.CharField(max_length=20)
    is_staff = serializers.BooleanField(default=False)
    is_active = serializers.BooleanField(default=True)
    Phone = serializers.CharField(max_length=15)
    PhoneValidate = serializers.BooleanField(default=False)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
    Location = serializers.CharField(max_length=100, default='')
    Avatar = serializers.ImageField(default=None)

    def create(self, validated_data):
        return PersonalData.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.Surname = validated_data.get('Surname', instance.Surname)
        instance.Name = validated_data.get('Name', instance.Name)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.Phone = validated_data.get('Phone', instance.Phone)
        instance.PhoneValidate = validated_data.get('PhoneValidate', instance.PhoneValidate)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.Location = validated_data.get('Location', instance.Location)
        instance.Avatar = validated_data.get('Avatar', instance.Avatar)
        instance.save()
        return instance

class PhoneCode_ValidationSend(serializers.Serializer): # сериалайзер для персональных данных

    Phone = serializers.CharField(max_length=15)

    def update(self, instance, validated_data):
        instance.Phone = validated_data.get('Phone', instance.Phone)
        instance.save()
        return instance

class PhoneCode_Validate(serializers.Serializer): # сериалайзер для персональных данных

    Phone = serializers.CharField(max_length=15)
    PhoneCode = serializers.CharField(default='', max_length=4)

    def update(self, instance, validated_data):
        instance.Phone = validated_data.get('Phone', instance.Phone)
        instance.PhoneCode = validated_data.get('PhoneCode', instance.PhoneCode)
        instance.save()
        return instance

class EmailCodeValidate(serializers.Serializer): # сериалайзер для персональных данных

    Email = serializers.CharField(max_length=15)
    EmailValidate = serializers.CharField(default='', max_length=4)

    def update(self, instance, validated_data):
        instance.Email = validated_data.get('Email', instance.Email)
        instance.EmailValidate = validated_data.get('EmailValidate', instance.EmailValidate)
        instance.save()
        return instance

class MessagesSerializer(serializers.Serializer):

    FirstPhone = serializers.CharField(max_length=20)
    SecondPhone = serializers.CharField(max_length=20)
    Chat = serializers.CharField(max_length=700000)

    def create(self, validated_data):
        return Message.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.FirstPhone = validated_data.get('FirstPhone', instance.FirstPhone)
        instance.SecondPhone = validated_data.get('SecondPhone', instance.SecondPhone)
        instance.Chat = validated_data.get('Chat', instance.Chat)
        instance.save()
        return instance

class DialogCreate(serializers.Serializer):

    FirstPhone = serializers.CharField(max_length=20)
    SecondPhone = serializers.CharField(max_length=20)

    def create(self, validated_data):
        return Message.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.FirstPhone = validated_data.get('FirstPhone', instance.FirstPhone)
        instance.SecondPhone = validated_data.get('SecondPhone', instance.SecondPhone)
        instance.save()
        return instance
