from django.core.management.base import BaseCommand, CommandError
from ...models import Game
from ...hblib import HumbleBundle

class Command(BaseCommand):
    # def add_arguments(self, parser):
        # Positional arguments
        # parser.add_argument('poll_ids', nargs='+', type=int)

        # Named (optional) arguments
        # parser.add_argument(
        #     '--delete',
        #     action='store_true',
        #     help='Delete poll instead of closing it',
        # )

    def handle(self, *args, **options):
        # ...
        # if options['delete']:
        #     poll.delete()
        # ...

        hb = HumbleBundle()
        hb.login()

        print('getting games')
        games = hb.get_keys()

        print('save to database')
        # game_objects = Game.objects.bulk_create(games, 100, True)
        for game in games:
            game.save()
            print(f'saved {game}')
        
        



