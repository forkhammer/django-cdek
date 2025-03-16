from django.core.management.base import BaseCommand

from djcdek.cdek.utils.update import update_regions, update_cities, update_pvz


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        update_regions()
        update_cities()
        update_pvz()

