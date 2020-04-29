from django.contrib import admin

from . import models

admin.site.register(models.Supplier)
admin.site.register(models.Item)
admin.site.register(models.OrderItem)
admin.site.register(models.Order)
admin.site.register(models.UserDeliveryDetail)
admin.site.register(models.Payment)
