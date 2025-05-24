from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = "Удаляет все данные и создаёт тестовые категории и продукты"

    def handle(self, *args, **kwargs):
        # Удаление всех данных
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создание категорий
        books = Category.objects.create(name="Книги", description="Художественная литература")
        electronics = Category.objects.create(name="Электроника", description="Гаджеты и техника")
        toys = Category.objects.create(name="Игрушки", description="Для детей и взрослых")

        # Создание продуктов
        Product.objects.create(
            name="Гарри Поттер",
            description="Фэнтези роман",
            purchase_price=750.00,
            category=books
        )
        Product.objects.create(
            name="Война и мир",
            description="Классика русской литературы",
            purchase_price=500.00,
            category=books
        )
        Product.objects.create(
            name="Смартфон",
            description="Мощный телефон",
            purchase_price=25000.00,
            category=electronics
        )
        Product.objects.create(
            name="Игрушечный робот",
            description="Интерактивная игрушка",
            purchase_price=1800.00,
            category=toys
        )

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно добавлены."))
