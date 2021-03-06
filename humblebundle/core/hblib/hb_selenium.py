

from lib2to3.pgen2 import driver
from platform import platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint
from time import sleep
from dotenv import load_dotenv
import os
import json
from ..models import Game

load_dotenv()

BASE_URL = 'https://www.humblebundle.com'
ORDERS = 'https://www.humblebundle.com/api/v1/user/order'
ORDERS_DETAILS = 'https://www.humblebundle.com/api/v1/orders?all_tpkds=true&gamekeys=Pd3yaUzfUEe2Xzhf&gamekeys=hn2uW8Kpe4XT75Dz&gamekeys=76vhyUqM4y6nwRby&gamekeys=VseEKV5thcc8577m&gamekeys=tpruBqvqvaFtWkPA&gamekeys=Y3F3qfauqaF6kA8A&gamekeys=466EA5A6Rx4yNH4u&gamekeys=wHMYGsT74q8dbBE2&gamekeys=M2wZZvUPV7y853YS&gamekeys=yU6FNfNVMMuV8Ztx&gamekeys=rxhVtaAqXPddrYFz&gamekeys=bm5YUAabtrFHbPN3&gamekeys=AnN4xCFWqfGPx3WF&gamekeys=cfHRSdyxsBFPftFA&gamekeys=uz62zHmSumhGvNss&gamekeys=b6pkxyK8kMaEuU7p&gamekeys=q7VtwRqfcDKV3kNT&gamekeys=yPHwurnGswNMycMb&gamekeys=ckGpnppx4B7V7wA3&gamekeys=tzDdrsHketVWRz7F&gamekeys=nyvyYV7r2WFP8KpY&gamekeys=fTRzUu2u2UyrwDC3&gamekeys=DsFHz8Mt4xPDfvyK&gamekeys=yfsnceXp6spaaxBD&gamekeys=Ws6RB4UyMFm2zva5&gamekeys=Ar2G6UqVEAF72mT3&gamekeys=cqsaZBrkazFV8aTC&gamekeys=S6nVrEZSWwY7Hs8U&gamekeys=a3mRA4DuVdqNMZPm&gamekeys=RW8ZVwpc4PAF8cWC&gamekeys=Xtz6zbXbvhCKRNZv&gamekeys=hz6XvvqPdBSeqESV&gamekeys=yupENF4Ba4RhwEDc&gamekeys=dZz82yvqedDhFxAq&gamekeys=H4PyBrDs4NzKV38S&gamekeys=2u8rHD6dVXMxS5F4&gamekeys=GBbVxaaFeXFw3XnE&gamekeys=2fGxTqkymsDpDMbP&gamekeys=vFrf7uppMc7cvuRc&gamekeys=fXn8vevpkpDH2CHp'
PURCHASES = 'https://www.humblebundle.com/home/purchases'
KEYS = 'https://www.humblebundle.com/home/keys'


class HumbleBundle():
    def __init__(self):
        # self.driver = webdriver.Firefox()
        USER_DATA_DIR = "C:\\Users\\henri\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 3"
        chrome_options = Options()
        chrome_options.add_argument(f'--user-data-dir={USER_DATA_DIR}')
        # chrome_options.add_argument(f'--profile-directory={USER_DATA_DIR}')
        # chrome_options.add_argument(f'--profile-directory="Profile 3"')
        self.driver = webdriver.Chrome(options=chrome_options)

        self.choices_urls = []

    def login(self):
        self.driver.get(BASE_URL+'/login')
        
        # Already logged in
        if self.driver.current_url == 'https://www.humblebundle.com/home/library':
            self.is_logged_in = True
            return

        # Do log in
        USERNAME = os.getenv('USERNAME')
        username_input = self.driver.find_element_by_name('username')
        username_input.send_keys(USERNAME)
        
        PASSWORD = os.getenv('PASSWORD')
        password_input = self.driver.find_element_by_name('password')
        password_input.send_keys(PASSWORD)

        password_input.send_keys(Keys.RETURN)

        # Just do an input here for 2fa ++
        input('Press enter when logged in.')
        self.is_logged_in = True

        return

    def get_purchases(self):
        self.driver.get(PURCHASES)

        wait = WebDriverWait(self.driver, 1000)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'row')))

        elems = self.driver.find_elements(By.CLASS_NAME, 'row')
        for elem in elems:
            print(elem.text)
            pprint(elem)
            elem.click
            sleep(10)

    def get_keys(self):
        print('Get keys')
        self.driver.get(KEYS)

        wait = WebDriverWait(self.driver, 500)

        print('Hide redeemed keys')
        # click to hide redeemed keys
        hide_redeemed = "xpath=//label[contains(.,'Hide redeemed keys & entitlements')]"
        wait.until(EC.presence_of_element_located((By.ID, 'hide-redeemed')))
        self.driver.find_element(By.ID, "hide-redeemed").click()

        print('wait for table')
        # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'unredeemed-keys-table')))
        sleep(2)

        print('Has next?')
        has_next = True

        scraped_data = []

        while has_next:
            pagination = self.driver.find_element(By.CLASS_NAME, 'pagination')
            try:
                next = pagination.find_element(By.CLASS_NAME, 'hb-chevron-right')
                has_next = True
            except:
                print('Does not have next...')
                has_next = False

            print('scrolling')
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            self.driver.execute_script("window.scrollTo(0, 0)")

            # self.driver.implicitly_wait(10)

            table = self.driver.find_element(By.CLASS_NAME, 'unredeemed-keys-table')
            tbody = table.find_element(By.TAG_NAME, 'tbody')

            rows = tbody.find_elements(By.TAG_NAME, 'tr')

            for row in rows:
                tds = row.find_elements(By.TAG_NAME, 'td')
                
                platform = None
                platform = row.find_element(By.CLASS_NAME, 'platform').text
                print(f'{platform=}')

                gamename_title = None
                gamename_element = row.find_element(By.CLASS_NAME, 'game-name')
                gamename_title = gamename_element.find_element(By.TAG_NAME, 'h4').text
                print(f'{gamename_title=}')
                
                gamename_p = None
                try:
                    gamename_p = gamename_element.find_element(By.TAG_NAME, 'p').text
                    print(f'{gamename_p=}')
                except:
                    pass
                print(f'{gamename_p=}')


                gamename_link_text = None
                gamename_link_href = None
                try:
                    gamename_link = gamename_element.find_element(By.TAG_NAME, 'a')
                    gamename_link_text = gamename_link.text
                    gamename_link_href = gamename_link.get_attribute('href')
                except:
                    pass
                print(f'{gamename_link_text=}')
                print(f'{gamename_link_href=}')


                choice_url = None
                try:
                    choice_url = row.find_element(By.CLASS_NAME, 'choice-button').get_attribute('href')
                except:
                    pass
                print(f'{choice_url=}')
                

                scraped_data.append(
                    Game(
                        platform=platform,
                        title=gamename_title,
                        paragraph=gamename_p,
                        game_link_text=gamename_link_text,
                        game_link_href=gamename_link_href,
                        choice_url=choice_url,
                        is_redeemed=False
                    )
                )

            if has_next:
                print('Next page!')
                next.click()
            
        pprint(scraped_data)

        # with open('get_keys_1.json', 'w') as json_file:
        #     json.dump(scraped_data, json_file)

        for game in scraped_data:
            if game.platform == 'HUMBLE BUNDLE':
                choices = self.get_unredeemed_choices(game['choice_url'])
                scraped_data.extend(choices)

        return scraped_data
        

    def get_unredeemed_choices(self, choice_url):
        print('Get unredeemed choices')
        self.driver.get(choice_url)

        wait = WebDriverWait(self.driver, 500)

        print('wait for table')
        # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'unredeemed-keys-table')))
        sleep(2)

        choices = self.driver.find_elements(By.CLASS_NAME, 'content-choice')

        scraped_data = []

        for choice in choices:
            classes = choice.get_attribute('class')
            print(f'{classes=}')

            is_redeemed = False
            if 'claimed' in classes:
                is_redeemed = True
            
            # title
            title_elem = choice.find_element(By.CLASS_NAME, 'content-choice-title')
            title = title_elem.text
            gamename_link_href = self.driver.current_url
            
            # platform
            delivery_methods_elem = choice.find_element(By.CLASS_NAME, 'delivery-methods')
            platform_element = delivery_methods_elem.find_element(By.TAG_NAME, 'i')
            platform = platform_element.get_attribute('aria-label')
            scraped_data.append(
                Game(
                    platform=platform,
                    title=title,
                    paragraph=None,
                    game_link_text=None,
                    game_link_href=gamename_link_href,
                    choice_url=gamename_link_href,
                    is_redeemed = is_redeemed
                )
            )
            
        pprint(scraped_data)

        # print('save to json')
        # filename = gamename_link_href.replace(':', '').replace('/','-').replace('.', '-')
        # with open(f'{filename}.json', 'w') as json_file:
        #     json.dump(scraped_data, json_file, indent=4)
        # print('saved')

        # print('Bulk create to database')
        # Game.objects.bulk_create(scraped_data, batch_size=100, ignore_conflicts=True)        
        return scraped_data


    def get_drmfree_from_purchases(self):
        print('Get drm free')
        self.driver.get(PURCHASES)

        # when using wait, time out after 3 seconds
        wait = WebDriverWait(self.driver, 3)

        # All the keys to loop
        keys = []
        # The result to return
        result = []

        # Loop pages and get keys
        print('looping purchase pages')
        has_next = True
        while has_next:

            # Entire site is js hidden and shown
            # purchase site is js-purchase-holder

            purchase_holder = self.driver.find_element(By.CLASS_NAME, 'js-purchase-holder')

            page_keys = []
            print('getting keys from page')
            rows = purchase_holder.find_elements(By.CLASS_NAME, 'row')
            for row in rows:
                key = row.get_attribute('data-hb-gamekey')
                page_keys.append(key)

            print('Page keys:')
            pprint(page_keys)
            keys.extend(page_keys)

            print('find pagination and next button')
            pagination = purchase_holder.find_element(By.CLASS_NAME, 'pagination')
            try:
                next = pagination.find_element(By.CLASS_NAME, 'hb-chevron-right').click()
            except:
                print('Does not have next...')
                has_next = False

        print('Looping keys...')
        for key in keys:
            url = f'https://www.humblebundle.com/downloads?key={key}'
            self.driver.get(url)
            print("\n\n")
            print(url)
            print("\n\n")

            self.driver.execute_script("window.scrollTo(0, 500)")

            sleep(0.5)

            print('wait for download')
            try:
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'js-all-downloads-holder')), "message string on wait until")
                print('Found downloads holder')
            except Exception as e:
                print('no downloads found')
                print(e)
                print('continue')
                continue

            js_all_downloads_holder_elem = self.driver.find_element(By.CLASS_NAME, 'js-all-downloads-holder')

            # can have multiple downloads row, game, audio, ebook, etc
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'wrapper')), "No wrapper?")
            wrapper_elems = js_all_downloads_holder_elem.find_elements(By.CLASS_NAME, 'wrapper')
            print(f'wrapper_elems: {wrapper_elems}')

            if len(wrapper_elems) == 0:
                input('why is wrapper 0?')

            # wrapper
            print('for wrapper_elem in wrapper_elems')
            for wrapper_i in range(len(js_all_downloads_holder_elem.find_elements(By.CLASS_NAME, 'wrapper'))):
                wrapper_elem = js_all_downloads_holder_elem.find_elements(By.CLASS_NAME, 'wrapper')[wrapper_i]
                print('wrapper...')

                # get platforms
                platform_elems = wrapper_elem.find_element(By.CLASS_NAME, 'dlplatform-list').find_elements(By.CLASS_NAME, 'js-platform-button')

                # wrapper dict
                temp_dict = {}

                # for platform, for dltype
                print('for platform, for dltype')
                for platform_i in range(len(platform_elems)):
                    wrapper_elem = js_all_downloads_holder_elem.find_elements(By.CLASS_NAME, 'wrapper')[wrapper_i]
                    platform_elems = wrapper_elem.find_element(By.CLASS_NAME, 'dlplatform-list').find_elements(By.CLASS_NAME, 'js-platform-button')
                    platform_elem = platform_elems[platform_i]
                    print(f'clicking {platform_elem.text=}')
                    platform_elem.click()

                    # get download types
                    # Get inside platform to escape stale elements
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dltype')))
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'flexbtn')))
                    dltype_elems = wrapper_elem.find_element(By.CLASS_NAME, 'dltype').find_elements(By.CLASS_NAME, 'flexbtn')

                    for dltype_elem in dltype_elems:
                        print(f'clicking {dltype_elem.text=}')
                        platform_elem.click()

                        current_platform = platform_elem.get_attribute('data-platform')
                        current_dltype = dltype_elem.get_attribute('data-type')
                        current_platform_dltype_combo = f'{current_platform}_{current_dltype}'

                        # Get game, platform, dl_link
                        rows = wrapper_elem.find_elements(By.CLASS_NAME, 'row')
                        print('for row in rows')
                        for row in rows:
                            title = row.find_element(By.CLASS_NAME, 'title').text
                            print(f'{title=}')
                            subtitle = row.find_element(By.CLASS_NAME, 'subtitle').text
                            print(f'{subtitle=}')

                            download = row.find_element(By.CLASS_NAME, 'js-start-download')
                            download_href = download.find_element(By.TAG_NAME, 'a').get_attribute('href')
                            print(f'{download_href=}')


                            if title not in temp_dict.keys():
                                print(f'adding {title} to temp_dict')
                                temp_dict[title] = {}
                                temp_dict[title]['title'] = title
                                temp_dict[title]['subtitle'] = subtitle

                            if 'drm_free_links' not in temp_dict[title]:
                                temp_dict[title]['drm_free_links'] = {}
                            temp_dict[title]['drm_free_links'][current_platform_dltype_combo] = download_href

                            if current_platform not in temp_dict[title]['drm_free_links']:
                                temp_dict[title]['drm_free_links'][current_platform] = {}
                            temp_dict[title]['drm_free_links'][current_platform][current_dltype] = download_href

                            temp_dict[title]['humble_bundle_page_link'] = url

                            print(f'tempdict for {title}')
                            pprint(temp_dict[title])
                        
                wrapper_dict = temp_dict

                print('wrapper dict')
                pprint(wrapper_dict)

                print('wrapper dict values')
                pprint(wrapper_dict.values())

                result.extend(wrapper_dict.values())

                print('result')
                pprint(result, indent=2)

        return result

if __name__ == '__main__':
    hb = HumbleBundle()
    hb.login()
    # hb.get_keys()
    hb.get_drmfree_from_purchases()

