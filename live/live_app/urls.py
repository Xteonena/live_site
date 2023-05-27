from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, PropertyTypeViewSet, RegisterView, LoginView, PropertyImageViewSet, CommentViewSet, \
    UserViewSet
from . import views
from .consumers import ChatConsumer

router = DefaultRouter()
router.register(r'properties', PropertyViewSet)
router.register(r'propertytypes', PropertyTypeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'propertyimages', PropertyImageViewSet)
router.register(r'chats', views.ChatViewSet)
router.register(r'messages', views.MessageViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('ws/chat/', ChatConsumer.as_asgi()),
] + router.urls
