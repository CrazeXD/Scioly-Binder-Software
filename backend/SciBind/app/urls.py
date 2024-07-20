from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Binders, Events
from .views import register, login, logout

router = DefaultRouter()
router.register(r'binders', Binders, basename='binders')
router.register(r'events', Events, basename='events')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register),
    path('login/', login),
    path('logout/', logout)
]