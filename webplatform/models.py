from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

class Supplier(models.Model):
    business_name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    contact_address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name

class Item(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    minimum_portions = models.IntegerField(blank=True, null=True)
    portion_increment = models.IntegerField(blank=True, null=True)
    minimum_lead_time = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_add_to_order_url(self):
        return reverse("webplatform:add_to_order", kwargs={'pk': self.pk})

    def get_remove_from_order_url(self):
        return reverse("webplatform:remove_from_order", kwargs={'pk': self.pk})

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.item.name} (quantity: {self.quantity})'

    def get_total_item_price(self):
        return self.quantity * self.item.price

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    price = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.stripe_charge_id)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    delivery_date = models.DateField(null=True, default=timezone.now)
    delivery_time = models.TimeField(null=True, default=timezone.now)
    is_completed = models.BooleanField(default=False)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    def get_total_order_price(self):
        total_order_price = 0
        for item in self.items.all():
            total_order_price += item.get_total_item_price()
        return total_order_price

class UserDeliveryDetail(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    instructions = models.TextField()

    def __str__(self):
        return self.user.email
