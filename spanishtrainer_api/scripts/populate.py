from django.core.management.base import BaseCommand

from spanishtrainer_api.models import Category


# class Command(BaseCommand):
#     help = 'Creates application data'

 # def handle(self, *args, **kwargs):
 #     pass
    # get or create superuser
    # user = User.objects.filter(username='admin').first()
    # if not user:
    #     user = User.objects.create_superuser(username='admin', password='test')

    # example
    # Product(name="Coffee Machine", description=lorem_ipsum.paragraph(), price=Decimal('70.99'), stock=6),

    # create categorys
    # categorys = [
    #     Category(name_en="", name_de="", name_es="", parent=""),
    # ]

    # create products & re-fetch from DB
    # Category.objects.bulk_create(categorys)
    # categorys = Category.objects.all()


    # create some dummy orders tied to the superuser
    # for _ in range(3):
    #     # create an Order with 2 order items
    #     order = Order.objects.create(user=user)
    #     for product in random.sample(list(products), 2):
    #         OrderItem.objects.create(
    #             order=order, product=product, quantity=random.randint(1,3)
    #         )