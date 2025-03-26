from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class UserProfileRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email','password' ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
            user = UserProfile.objects.create_user(**validated_data)
            return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'email': {
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'brand_name']


class ModelSerializer(serializers.ModelSerializer):
    brand_model = BrandSerializer(many=True, read_only=True)
    class Meta:
        model = Model
        fields = ['id', 'model_name', 'brand_model']


class CarSimpleSerializer(serializers.ModelSerializer):
    brand_car = BrandSerializer(many=True, read_only=True)
    model_car = ModelSerializer(many=True, read_only=True)
    class Meta:
        model = Car
        fields = ['id', 'brand_car', 'model_car']


class CarListSerializer(serializers.ModelSerializer):
    brand_car = BrandSerializer(many=True, read_only=True)
    model_car = ModelSerializer(many=True, read_only=True)
    class Meta:
        model = Car
        fields = ['id', 'brand_car', 'model_car', 'year', 'fuel_type', 'transmission', 'mileage', 'price']


class CarDetailSerializer(serializers.ModelSerializer):
    seller = UserProfileSimpleSerializer()
    class Meta:
        model = Car
        fields = ['id', 'brand', 'model','image', 'year', 'description','fuel_type', 'transmission', 'mileage', 'price', 'seller']


class AuctionSerializer(serializers.ModelSerializer):
    car_auction = CarSimpleSerializer(many=True, read_only=True)
    start_time = serializers.DateTimeField(format='%d-%m_Y')
    end_time = serializers.DateTimeField(format='%d-%m_Y')
    class Meta:
        model = Auction
        fields = ['id', 'car_auction', 'start_price', 'min_price', 'start_time', 'end_time', 'status_auction']


class BidSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d-%m_Y')
    class Meta:
        model = Bid
        fields = ['id', 'auction', 'buyer', 'amount', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    seller = UserProfileSimpleSerializer()
    buyer = UserProfileSimpleSerializer()
    class Meta:
        model = Review
        fields = ['id', 'buyer', 'seller', 'text', 'stars']