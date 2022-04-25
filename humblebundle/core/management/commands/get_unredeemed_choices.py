from platform import platform
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

        choices = Game.objects.filter(platform='HUMBLE CHOICE')
        print(choices)

        if len(choices) == 0:
            return

        hb = HumbleBundle()
        hb.login()

        for choice_bundle in choices:
            print(choice_bundle)
            print(choice_bundle.choice_url)
            games = hb.get_unredeemed_choices(choice_bundle.choice_url)
            
            print('save to database')
            # game_objects = Game.objects.bulk_create(games, 100, True)
            for game in games:
                defaults = {
                    'platform': game.platform,
                    'title': game.title,
                    'paragraph': game.paragraph,
                    'game_link_text': game.game_link_text,
                    'game_link_href': game.game_link_href,
                    'choice_url': game.choice_url,
                    'is_redeemed': game.is_redeemed,
                }
                Game.objects.update_or_create(title=game.title, defaults=defaults)
                print(f'saved {game}')
        
        



