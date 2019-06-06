import graphene

from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from catalog.models import Category, Product


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        interfaces = (graphene.Node, )
        filter_fields = ['name',]

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        filter_fields = ['name', 'price']

class CartMutation(graphene.Mutation):

    class Arguments:
        product_id = graphene.Int(required=True)
        quantity = graphene.Int(required=True)

    result = graphene.Boolean()

    def mutate(self, info, product_id, quantity):
        # TODO: add products to cart using django.session
        return {'result': True}

class Mutation:
    add_to_cart = CartMutation.Field()

class Query:
    all_categories = DjangoFilterConnectionField(CategoryType)
    all_products = graphene.List(ProductType)

    category = graphene.Field(CategoryType, id=graphene.Int(), name=graphene.String())
    product = graphene.Field(ProductType, id=graphene.Int())

    def resolve_all_products(self, info, **kwargs):
        return Product.objects.select_related('category').all()

    def resolve_category(self, info, **kwargs):
        if 'id' in kwargs:
            return Category.objects.get(id=kwargs['id'])
        if 'name' in kwargs:
            return Category.objects.get(name=kwargs['name'])
        return None

    def resolve_product(self, info, **kwargs):
        if 'id' in kwargs:
            return Product.objects.get(id=kwargs['id'])
        return None

