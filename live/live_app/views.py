from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import Property, PropertyType, Comment, Chat, Message
from .serializers import PropertySerializer, PropertyTypeSerializer, CommentSerializer, ChatSerializer, \
    MessageSerializer
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import PropertyImage
from .serializers import PropertyImageSerializer
from PIL import Image
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response


def resize_and_compress_image(image, max_size, quality):
    img = Image.open(image)

    if img.width > max_size or img.height > max_size:
        if img.width >= img.height:
            new_width = max_size
            new_height = int((max_size / img.width) * img.height)
        else:
            new_height = max_size
            new_width = int((max_size / img.height) * img.width)

        img = img.resize((new_width, new_height), Image.ANTIALIAS)

    img.save(image.path, optimize=True, quality=quality)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def get_user(self, request):
        username = request.query_params.get('username', None)
        if username is not None:
            users = User.objects.filter(username__icontains=username)
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PropertyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = PropertyPagination

    def get_queryset(self):
        user = self.request.user
        user_id = self.request.query_params.get('user_id', None)
        property_id = self.request.query_params.get('property_id', None)
        search_text = self.request.query_params.get('searchText', None)
        property_type = self.request.query_params.get('propertyType', None)
        min_price = self.request.query_params.get('minPrice', None)
        max_price = self.request.query_params.get('maxPrice', None)
        min_area = self.request.query_params.get('minArea', None)
        max_area = self.request.query_params.get('maxArea', None)
        min_rooms = self.request.query_params.get('minRooms', None)
        max_rooms = self.request.query_params.get('maxRooms', None)

        properties = Property.objects.all().order_by('id')

        if user_id is not None and user.id == int(user_id):
            properties = properties.filter(user=user)
        elif property_id is not None:
            properties = properties.filter(id=property_id)

        elif search_text is not None:  # обновлено
            properties = properties.filter(title__icontains=search_text)

        if property_type is not None:
            properties = properties.filter(property_type__name__icontains=property_type)
        if min_price is not None:
            properties = properties.filter(price__gte=min_price)
        if max_price is not None:
            properties = properties.filter(price__lte=max_price)
        if min_area is not None:
            properties = properties.filter(area__gte=min_area)
        if max_area is not None:
            properties = properties.filter(area__lte=max_area)
        if min_rooms is not None:
            properties = properties.filter(rooms__gte=min_rooms)
        if max_rooms is not None:
            properties = properties.filter(rooms__lte=max_rooms)

        return properties

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        self.queryset = self.queryset.filter(user=user)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        self.queryset = self.queryset.filter(user=user)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        self.queryset = self.queryset.filter(user=user)
        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data
        files = request.FILES

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        property_instance = serializer.save(user=request.user)

        for key, file in files.items():
            image_instance = PropertyImage.objects.create(property=property_instance, image=file)
            resize_and_compress_image(image_instance.image, max_size=800, quality=75)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def get_user_properties(self, request):
        user = request.user
        properties = Property.objects.filter(user=user).order_by('id')
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)


class PropertyTypeViewSet(viewsets.ModelViewSet):
    queryset = PropertyType.objects.all()  # добавьте сортировку
    serializer_class = PropertyTypeSerializer
    permission_classes = [permissions.AllowAny]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


class PropertyImageViewSet(viewsets.ModelViewSet):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        property_id = self.request.data.get('property_id')
        property_instance = Property.objects.get(id=property_id)

        # Get the initial data
        data = serializer.initial_data
        # Add the user data to the initial data
        data['user'] = UserSerializer(self.request.user).data
        # Create a new serializer with the updated data
        new_serializer = CommentSerializer(data=data)
        new_serializer.is_valid(raise_exception=True)
        # Save the new serializer
        new_serializer.save(user=self.request.user, property=property_instance)


class LoginView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.id})
        else:
            return Response({'error': 'Wrong credentials'}, status=status.HTTP_400_BAD_REQUEST)


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all().order_by('id')
    serializer_class = ChatSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(users=[self.request.user])


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
