from datetime import datetime, timedelta
from django.db import models
from django.utils.timezone import now
from django.utils.functional import cached_property

class City(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Города"

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey("City", related_name="suppliers", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    field = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    supplier = models.ForeignKey(Supplier, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @cached_property
    def new_orders(self):
        orders = []
        for order in self.orders.all():
            if now() - order.created > timedelta(minutes=15):
                orders.append(order)
        return orders

class OrderProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return '{} Product {} in order {}'.format(
            self.quantity,
            self.product_id,
            self.order_id
        )

class Order(models.Model):
    user_email = models.EmailField()
    products = models.ManyToManyField(
        Product,
        through=OrderProducts,
        related_name="orders"
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Order {} from {}'.format(
            self.id,
            self.user_email
        )

class CurrencyRate(models.Model):

    CURRENCIES = (
        ('usd', 'usd'),
        ('eur', 'eur')
    )

    currency = models.CharField(max_length=3, choices=CURRENCIES)
    rate = models.DecimalField(max_digits=10, decimal_places=6, default=1)

    def __str__(self):
        return "{} ({})".format(self.currency, self.rate)

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                rate = CurrencyRate.objects.get(currency=self.currency)
                self.pk = rate.pk
            except CurrencyRate.DoesNotExist:
                pass
        super().save(*args, **kwargs)
            