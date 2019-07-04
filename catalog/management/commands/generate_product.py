from django.core.management.base import BaseCommand

from catalog.models import (
    Product, 
    Supplier,
    City,
    Category,
)

from faker import Faker
import random
import factory
from factory.fuzzy import FuzzyDecimal


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Category %d' % n)

    class Meta:
        model = Category

class SupplierFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Supplier %d' % n)

    class Meta:
        model = Supplier



class ProductFactory(factory.django.DjangoModelFactory):

    price = FuzzyDecimal(1.0, 1000)
    name = factory.Sequence(lambda n: 'Product %d' % n)
    supplier = factory.SubFactory(SupplierFactory)

    class Meta:
        model = Product

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for categories in extracted:
                self.categories.add(category)


class Command(BaseCommand):

    def generate(self, amount=100):
        fake = Faker()

        categories = Category.objects.values_list('id', flat=True)
        suppliers = list(Supplier.objects.values_list('id', flat=True))

        for i in range(amount):
            p = ProductFactory.create(
                categories=set(random.sample(categories, 2))
            )

    def handle(self, *args, **kwargs):
        self.generate()
