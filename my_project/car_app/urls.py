from rest_framework import routers
from django.urls import path, include
from .views import *


router = routers.SimpleRouter()
router.register(r'users', UserProfileViewSet, basename='user_list')
router.register(r'brands', BrandVIewSet, basename='brand_list')
router.register(r'models', ModelVIewSet, basename='model_list')
router.register(r'bids', BidVIewSet, basename='bid_list')


urlpatterns = [
    path('', include(router.urls)),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('cars/', CarListApiVIew.as_view(), name = 'car_list'),
    path('cars/<int:pk>/', CarDetailApiVIew.as_view(), name='car_detail'),
    path('reviews/', ReviewApiVIew.as_view(), name = 'reviews'),
    path('reviews/create', ReviewCreateApiVIew.as_view(), name='review_create')
]
