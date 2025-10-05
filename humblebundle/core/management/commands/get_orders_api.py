from platform import platform
from django.core.management.base import BaseCommand, CommandError
from ...models import Game, Purchase
from ...hblib.hb_api import HumbleBundle


class Command(BaseCommand):
    def handle(self, *args, **options):
        # PLATFORM = "DRM FREE"

        hb = HumbleBundle()
        hb.login()
        hb.get_orders()
        # purchases = hb.get_purchases()
        # p_objs = []

        # print('save to database')
        # for p in purchases:
        #     purchase = Purchase(**p)
        #     p_objs.append(purchase)
        # Purchase.objects.bulk_create(p_objs, batch_size=100, ignore_conflicts=True)
