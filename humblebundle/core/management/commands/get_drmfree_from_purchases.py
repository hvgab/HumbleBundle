from platform import platform
from django.core.management.base import BaseCommand, CommandError
from ...models import Game
from ...hblib import HumbleBundle

class Command(BaseCommand):

    def handle(self, *args, **options):

        PLATFORM = 'DRM FREE'

        hb = HumbleBundle()
        hb.login()
        drm_free_games = hb.get_drmfree_from_purchases()

        print('save to database')
        for game in drm_free_games:
                defaults = {
                    'platform': PLATFORM,
                    'title': game['title'],
                    'subtitle': game['subtitle'],
                    'drm_free_dl_links': game['drm_free_links'],
                    'game_link_href': game['humble_bundle_page_link']
                }
                game_obj, created = Game.objects.update_or_create(title=game['title'], platform=PLATFORM, defaults=defaults)
                print(f'saved {game_obj}. created {created}')

        
        



