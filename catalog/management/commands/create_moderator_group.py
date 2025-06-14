from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product

class Command(BaseCommand):
    help = 'Создаёт группу Модератор продуктов с нужными правами'

    def handle(self, *args, **options):
        group_name = 'Модератор продуктов'
        group, created = Group.objects.get_or_create(name=group_name)

        content_type = ContentType.objects.get_for_model(Product)

        # Разрешение can_unpublish_product (кастомное)
        can_unpublish_perm = Permission.objects.get(
            codename='can_unpublish_product',
            content_type=content_type
        )

        # Разрешение на удаление продуктов
        delete_perm = Permission.objects.get(
            codename='delete_product',
            content_type=content_type
        )

        group.permissions.add(can_unpublish_perm, delete_perm)
        group.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" успешно создана и права назначены.'))
        else:
            self.stdout.write(self.style.WARNING(f'Группа "{group_name}" уже существует, права обновлены.'))
