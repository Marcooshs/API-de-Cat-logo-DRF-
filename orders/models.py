from django.conf import settings
from django.db import models
from decimal import Decimal
from django.db.models import Q


class Order(models.Model):
    class Status(models.TextChoices):
        CART = 'CART', 'cart'
        PENDING = 'PENDING', 'Pending'
        PAID = 'PAID', 'Paid'
        SHIPPED = 'SHIPPED', 'Shipped'
        CANCELLED = 'CANCELLED', 'Cancelled'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name= 'orders')
    status = models.CharField(max_length= 20, choices= Status.choices, default= Status.CART)
    total_amount = models.DecimalField(max_digits= 12, decimal_places= 2, default= Decimal('0.00'))
    shipping_address = models.TextField(blank= True)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)


    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields= ['status', 'user'])]

    def __str__(self):
        return f'Order #{self.pk} - {self.user} - {self.status}'

    def recalc_total(self, save= True):
        total = Decimal('0.00')
        for it in self.items.all():
            total += it.unit_price * it.quantity
        self.total_amount = total
        if save:
            self.save(update_fields= ['total_amount', 'updated_at'])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete= models.CASCADE, related_name= 'items')
    product = models.ForeignKey('catalog.Product', on_delete= models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits= 12, decimal_places= 2)


    class Meta:
        unique_together = [('order', 'product')]
        constraints = [
            models.CheckConstraint(condition=Q(quantity__gte=1), name="orderitem_quantity_gte_1"),
        ]

    def __str__(self):
        return f'{self.product} x {self.quantity}'

    @property
    def line_total(self):
        return self.unit_price * self.quantity
