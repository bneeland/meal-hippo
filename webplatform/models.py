from django.db import models
from django.conf import settings
from django.urls import reverse
from datetime import time

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
    calories = models.CharField(max_length=100, blank=True, null=True)
    protein = models.FloatField(blank=True, null=True)
    fat = models.FloatField(blank=True, null=True)
    carbs = models.FloatField(blank=True, null=True)
    portion_size = models.TextField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField()
    is_featured = models.BooleanField(default=False)
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
    is_individual = models.BooleanField(default=False)
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
    to_be_delivered = models.BooleanField(default=True)
    delivery_date = models.DateField(null=True)
    delivery_time = models.TimeField(null=True)
    is_completed = models.BooleanField(default=False)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    def get_order_initial_subtotal(self):
        order_initial_subtotal = 0
        for item in self.items.all():
            order_initial_subtotal += item.get_total_item_price()
        return order_initial_subtotal

    def get_order_web_fee(self):
        order_initial_subtotal = self.get_order_initial_subtotal()
        # Set web fees
        website_fee_fixed = 3
        website_fee_variable = 0.029
        # Apply web fees
        order_web_fee = website_fee_fixed + order_initial_subtotal * website_fee_variable
        return order_web_fee

    def get_order_subtotal(self):
        order_initial_subtotal = self.get_order_initial_subtotal()
        order_web_fee = self.get_order_web_fee()
        order_subtotal = order_initial_subtotal + order_web_fee
        # Delivery fee (only if user's setting is not set to free delivery)
        if not UserDeliveryDetail.objects.filter(user=self.user)[0].free_delivery and self.to_be_delivered:
            # Set delivery fee
            order_delivery_fee = 6
            # Apply delivery fee
            order_subtotal += order_delivery_fee
        return order_subtotal

    def get_order_gst(self):
        order_subtotal = self.get_order_subtotal()
        gst_rate = 0.05
        order_gst = order_subtotal * gst_rate
        return order_gst

    def get_order_total(self):
        order_subtotal = self.get_order_subtotal()
        order_gst = self.get_order_gst()
        order_total = order_subtotal + order_gst
        return order_total

class UserDeliveryDetail(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    instructions = models.TextField(blank=True, null=True)
    free_delivery = models.BooleanField(default=True)
    is_subscribed = models.BooleanField(default=False, verbose_name='subscribe weekly')

    def __str__(self):
        return self.user.email

class UserSubscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_subscribed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

class Feedback(models.Model):
    FEEL_CHOICES = (
        ('VD', 'Very disappointed'),
        ('SD', 'Somewhat disappointed'),
        ('ND', 'Not disappointed'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    feel_if_no_longer = models.CharField(max_length=2, choices=FEEL_CHOICES, default=None, verbose_name='How would you feel if you could no longer use Meal Hippo?')
    type_of_people = models.TextField(verbose_name='What type of people do you think would most benefit from Meal Hippo?')
    main_benefit = models.TextField(verbose_name='What is the main benefit you receive from Meal Hippo?')
    how_to_improve = models.TextField(verbose_name='How can we improve Meal Hippo for you?')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.email
