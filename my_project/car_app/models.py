from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField


STATUS_CHOICES = (
    ('admin', 'admin'),
    ('seller', 'seller'),
    ('buyer', 'buyer')
)

FUEL_TYPE = (
    ('Бензин', 'Бензин'),
    ('Дизель', 'Дизель'),
    ('Газ', 'Газ'),
    ('Электро', 'Электро'),
    ('Гибрид', 'Гибрид'),
)

TYPE_TRANSMISSION = (
    ('Автомат', 'Автомат'),
    ('Механика', 'Механика')
)

STATUS_AUCTION = (
    ('активен', 'активен'),
    ('завершен', 'завершен'),
    ('отменен', 'отменен')
)


class UserProfile(AbstractUser):
    role = models.CharField(choices=STATUS_CHOICES, max_length=10, default='buyer')
    phone_number = PhoneNumberField(region='KG')

    def __str__(self):
        return self.first_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=34, unique=True)

    def __str__(self):
        return self.brand_name


class Model(models.Model):
    model_name = models.CharField(max_length=34, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_model')

    def __str__(self):
        return f'{self.model_name} - {self.brand}'


class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_car')
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='model_car')
    year = models.PositiveSmallIntegerField(default=0)
    fuel_type = MultiSelectField(choices=FUEL_TYPE, max_length=14)
    transmission = models.CharField(choices=TYPE_TRANSMISSION,max_length=12)
    mileage = models.PositiveSmallIntegerField(default=0)
    price = models.PositiveSmallIntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(upload_to='car_images/')
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='seller_car')

    def __str__(self):
        return f'{self.brand}-{self.model}'


class Auction(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE, related_name='car_auction')
    start_price = models.PositiveSmallIntegerField(default=0)
    min_price = models.PositiveSmallIntegerField(default=0)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    status_auction = models.CharField(choices=STATUS_AUCTION, default='активен', max_length=12)

    def __str__(self):
        return f'{self.car} - {self.start_price}'


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='auction_bid')
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='buyer_bid')
    amount = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='seller_review')
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='buyer_review')
    text = models.TextField()
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=0)

    def __str__(self):
        return f'{self.buyer}-{self.seller}'
