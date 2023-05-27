from rest_framework import serializers
from .models import Property, PropertyType, PropertyImage, Comment, Chat, Message
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = '__all__'


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ('image',)


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class CommentSerializer(serializers.ModelSerializer):
    user = UserNameSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'comment', 'created_at', 'updated_at')


class PropertySerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    property_type = serializers.PrimaryKeyRelatedField(queryset=PropertyType.objects.all())
    images = PropertyImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = ('id', 'title', 'property_type', 'price', 'area', 'rooms', 'floors', 'location', 'description',
                  'contact_info', 'user', 'created_at', 'updated_at', 'images', 'comments','owner')

    def create(self, validated_data):
        property_instance = Property.objects.create(**validated_data)
        return property_instance


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('id', 'users')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"