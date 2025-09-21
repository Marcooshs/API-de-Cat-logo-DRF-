from django.db import models
from django.utils.text import slugify
from django.db.models import Q


class Category(models.Model):
    name = models.CharField(max_length= 120, unique= True)
    slug = models.SlugField(max_length= 140, unique= True)
    parent = models.ForeignKey('self', null= True, blank= True, on_delete= models.SET_NULL, related_name= 'children')
    created_at = models.DateTimeField(auto_now_add= True)


    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(max_length= 50, unique= True)
    name = models.CharField(max_length= 180)
    slug = models.SlugField(max_length= 200, unique= True, blank= True)
    description = models.TextField(blank= True)
    price = models.DecimalField(max_digits= 12, decimal_places= 2)
    stock = models.PositiveIntegerField(default= 0)
    is_active = models.BooleanField(default= True)
    category = models.ForeignKey(Category, on_delete= models.PROTECT, related_name= 'products')
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)


    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
        ]
        constraints = [
            models.CheckConstraint(check=Q(price__gte=0), name="product_price_gte_0"),
            models.CheckConstraint(check=Q(stock__gte=0), name="product_stock_gte_0"),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.name}-{self.sku}')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.sku})'
