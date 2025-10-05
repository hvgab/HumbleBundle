from lib2to3.pgen2 import driver
from platform import platform

from pprint import pprint
from time import sleep
from dotenv import load_dotenv
import os
import json
from core.models import Game
import requests

load_dotenv()

BASE_URL = "https://www.humblebundle.com"
ORDERS = "https://www.humblebundle.com/api/v1/user/order"
ORDERS_DETAILS = "https://www.humblebundle.com/api/v1/orders?all_tpkds=true&gamekeys=Pd3yaUzfUEe2Xzhf&gamekeys=hn2uW8Kpe4XT75Dz&gamekeys=76vhyUqM4y6nwRby&gamekeys=VseEKV5thcc8577m&gamekeys=tpruBqvqvaFtWkPA&gamekeys=Y3F3qfauqaF6kA8A&gamekeys=466EA5A6Rx4yNH4u&gamekeys=wHMYGsT74q8dbBE2&gamekeys=M2wZZvUPV7y853YS&gamekeys=yU6FNfNVMMuV8Ztx&gamekeys=rxhVtaAqXPddrYFz&gamekeys=bm5YUAabtrFHbPN3&gamekeys=AnN4xCFWqfGPx3WF&gamekeys=cfHRSdyxsBFPftFA&gamekeys=uz62zHmSumhGvNss&gamekeys=b6pkxyK8kMaEuU7p&gamekeys=q7VtwRqfcDKV3kNT&gamekeys=yPHwurnGswNMycMb&gamekeys=ckGpnppx4B7V7wA3&gamekeys=tzDdrsHketVWRz7F&gamekeys=nyvyYV7r2WFP8KpY&gamekeys=fTRzUu2u2UyrwDC3&gamekeys=DsFHz8Mt4xPDfvyK&gamekeys=yfsnceXp6spaaxBD&gamekeys=Ws6RB4UyMFm2zva5&gamekeys=Ar2G6UqVEAF72mT3&gamekeys=cqsaZBrkazFV8aTC&gamekeys=S6nVrEZSWwY7Hs8U&gamekeys=a3mRA4DuVdqNMZPm&gamekeys=RW8ZVwpc4PAF8cWC&gamekeys=Xtz6zbXbvhCKRNZv&gamekeys=hz6XvvqPdBSeqESV&gamekeys=yupENF4Ba4RhwEDc&gamekeys=dZz82yvqedDhFxAq&gamekeys=H4PyBrDs4NzKV38S&gamekeys=2u8rHD6dVXMxS5F4&gamekeys=GBbVxaaFeXFw3XnE&gamekeys=2fGxTqkymsDpDMbP&gamekeys=vFrf7uppMc7cvuRc&gamekeys=fXn8vevpkpDH2CHp"
PURCHASES = "https://www.humblebundle.com/home/purchases"
KEYS = "https://www.humblebundle.com/home/keys"


class HumbleBundle:
    def __init__(self):
        self.session = requests.Session()

    def login(self):
        url = "https://www.humblebundle.com/processlogin"

        code = int(input("AUTH CODE: "))

        form_data = {
            "username": os.getenv("USERNAME"),
            "password": os.getenv("PASSWORD"),
            "code": code,
        }

        print("Form Data:")
        print(form_data)

        # Do log in
        r = self.session.post(url, data=form_data)

        print(r.content)
        print(r.cookies)
        print(r.ok)
        print(r.raw)

        self.is_logged_in = True

        return

    def get_orders(self):
        print("Get Orders")
        r = self.session.get("https://humblebundle.com/api/v1/user/order")
        for row in r.json():
            print(f"Order Gamekey: {row['gamekey']}")

    def get_order(self, gamekey):
        print(f"Get Order {gamekey}")
        r = self.session.get(f"https://humblebundle.com/api/v1/user/order/{gamekey}")
        pprint(r.json())
        input("Neste?")

    def get_purchases(self):
        print("Get Purchases")
        self.driver.get(PURCHASES)

        # when using wait, time out after 3 seconds
        wait = WebDriverWait(self.driver, 3)

        # All the keys to loop
        keys = []
        # The result to return
        result = []

        # Loop pages and get keys
        print("looping purchase pages")
        has_next = True
        while has_next:
            sleep(1)

            # Entire site is js hidden and shown
            # purchase site is js-purchase-holder

            purchase_holder = self.driver.find_element(
                By.CLASS_NAME, "js-purchase-holder"
            )

            page_keys = []
            print("getting keys from page")
            sleep(1)
            rows = purchase_holder.find_elements(By.CLASS_NAME, "row")
            for row in rows:
                print("\n\n")
                key = row.get_attribute("data-hb-gamekey")
                print(f"{key=}")
                product_name = row.find_element(By.CLASS_NAME, "product-name").text
                print(f"{product_name=}")
                order_placed = ""
                try:
                    order_placed = row.find_element(By.CLASS_NAME, "order-placed").text
                except Exception as e:
                    print("Error: ")
                    print(e)
                print(f"{order_placed=}")
                order_total = row.find_element(By.CLASS_NAME, "total").text
                print(f"{order_total=}")
                print("\n\n")

                page_keys.append(
                    {
                        "key": key,
                        "product_name": product_name,
                        "order_placed": order_placed,
                        "order_total": order_total,
                    }
                )

            keys.extend(page_keys)

            print("find pagination and next button")

            sleep(1)
            purchase_holder = self.driver.find_element(
                By.CLASS_NAME, "js-purchase-holder"
            )
            sleep(1)
            pagination = purchase_holder.find_element(By.CLASS_NAME, "pagination")
            sleep(1)
            try:
                next = pagination.find_element(
                    By.CLASS_NAME, "hb-chevron-right"
                ).click()
            except:
                print("Does not have next...")
                has_next = False

        return keys

    def get_keys(self):
        scraped_data = []
        scraped_data.append(
            Game(
                platform=platform,
                title="gamename_title",
                paragraph="gamename_p",
                game_link_text="gamename_link_text",
                game_link_href="gamename_link_href",
                choice_url="choice_url",
                is_redeemed=False,
            )
        )

        for game in scraped_data:
            if game.platform == "HUMBLE BUNDLE":
                choices = self.get_unredeemed_choices(game["choice_url"])
                scraped_data.extend(choices)

        return scraped_data

    def get_unredeemed_choices(self, choice_url):
        print("Get unredeemed choices")
        self.driver.get(choice_url)

        wait = WebDriverWait(self.driver, 500)

        print("wait for table")
        # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'unredeemed-keys-table')))
        sleep(2)

        choices = self.driver.find_elements(By.CLASS_NAME, "content-choice")

        scraped_data = []

        for choice in choices:
            classes = choice.get_attribute("class")
            print(f"{classes=}")

            is_redeemed = False
            if "claimed" in classes:
                is_redeemed = True

            # title
            title_elem = choice.find_element(By.CLASS_NAME, "content-choice-title")
            title = title_elem.text
            gamename_link_href = self.driver.current_url

            # platform
            delivery_methods_elem = choice.find_element(
                By.CLASS_NAME, "delivery-methods"
            )
            platform_element = delivery_methods_elem.find_element(By.TAG_NAME, "i")
            platform = platform_element.get_attribute("aria-label")
            scraped_data.append(
                Game(
                    platform=platform,
                    title=title,
                    paragraph=None,
                    game_link_text=None,
                    game_link_href=gamename_link_href,
                    choice_url=gamename_link_href,
                    is_redeemed=is_redeemed,
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
        print("Get drm free")
        self.driver.get(PURCHASES)

        # when using wait, time out after 3 seconds
        wait = WebDriverWait(self.driver, 3)

        # All the keys to loop
        keys = []
        # The result to return
        result = []

        # Loop pages and get keys
        print("looping purchase pages")
        has_next = True
        while has_next:
            # Entire site is js hidden and shown
            # purchase site is js-purchase-holder

            purchase_holder = self.driver.find_element(
                By.CLASS_NAME, "js-purchase-holder"
            )

            page_keys = []
            print("getting keys from page")
            rows = purchase_holder.find_elements(By.CLASS_NAME, "row")
            for row in rows:
                key = row.get_attribute("data-hb-gamekey")
                page_keys.append(key)

            print("Page keys:")
            pprint(page_keys)
            keys.extend(page_keys)

            print("find pagination and next button")
            pagination = purchase_holder.find_element(By.CLASS_NAME, "pagination")
            try:
                next = pagination.find_element(
                    By.CLASS_NAME, "hb-chevron-right"
                ).click()
            except:
                print("Does not have next...")
                has_next = False

        print("Looping keys...")
        for key in keys:
            url = f"https://www.humblebundle.com/downloads?key={key}"
            self.driver.get(url)
            print("\n\n")
            print(url)
            print("\n\n")

            self.driver.execute_script("window.scrollTo(0, 500)")

            sleep(0.5)

            print("wait for download")
            try:
                wait.until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "js-all-downloads-holder")
                    ),
                    "message string on wait until",
                )
                print("Found downloads holder")
            except Exception as e:
                print("no downloads found")
                print(e)
                print("continue")
                continue

            js_all_downloads_holder_elem = self.driver.find_element(
                By.CLASS_NAME, "js-all-downloads-holder"
            )

            # can have multiple downloads row, game, audio, ebook, etc
            wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "wrapper")),
                "No wrapper?",
            )
            wrapper_elems = js_all_downloads_holder_elem.find_elements(
                By.CLASS_NAME, "wrapper"
            )
            print(f"wrapper_elems: {wrapper_elems}")

            if len(wrapper_elems) == 0:
                input("why is wrapper 0?")

            # wrapper
            print("for wrapper_elem in wrapper_elems")
            for wrapper_i in range(
                len(
                    js_all_downloads_holder_elem.find_elements(By.CLASS_NAME, "wrapper")
                )
            ):
                wrapper_elem = js_all_downloads_holder_elem.find_elements(
                    By.CLASS_NAME, "wrapper"
                )[wrapper_i]
                print("wrapper...")

                # get platforms
                platform_elems = wrapper_elem.find_element(
                    By.CLASS_NAME, "dlplatform-list"
                ).find_elements(By.CLASS_NAME, "js-platform-button")

                # wrapper dict
                temp_dict = {}

                # for platform, for dltype
                print("for platform, for dltype")
                for platform_i in range(len(platform_elems)):
                    # get fresh elements
                    js_all_downloads_holder_elem = self.driver.find_element(
                        By.CLASS_NAME, "js-all-downloads-holder"
                    )
                    print(f"{wrapper_i=}")
                    wrapper_elem = js_all_downloads_holder_elem.find_elements(
                        By.CLASS_NAME, "wrapper"
                    )[wrapper_i]
                    print(f"{platform_i=}")
                    platform_elems = wrapper_elem.find_element(
                        By.CLASS_NAME, "dlplatform-list"
                    ).find_elements(By.CLASS_NAME, "js-platform-button")
                    platform_elem = platform_elems[platform_i]
                    print(f"clicking {platform_elem.text=}")
                    platform_elem.click()

                    # After click, get fresh elements again
                    print("Get fresh elems after click")
                    js_all_downloads_holder_elem = self.driver.find_element(
                        By.CLASS_NAME, "js-all-downloads-holder"
                    )
                    wrapper_elem = js_all_downloads_holder_elem.find_elements(
                        By.CLASS_NAME, "wrapper"
                    )[wrapper_i]
                    platform_elems = wrapper_elem.find_element(
                        By.CLASS_NAME, "dlplatform-list"
                    ).find_elements(By.CLASS_NAME, "js-platform-button")
                    platform_elem = platform_elems[platform_i]

                    # get download types
                    # Get inside platform to escape stale elements
                    wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, "dltype"))
                    )
                    wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, "flexbtn"))
                    )
                    dltype_elems = wrapper_elem.find_element(
                        By.CLASS_NAME, "dltype"
                    ).find_elements(By.CLASS_NAME, "flexbtn")

                    for dltype_elem in dltype_elems:
                        print(f"clicking {dltype_elem.text=}")
                        wait.until(EC.element_to_be_clickable(platform_elem))
                        platform_elem.click()

                        current_platform = platform_elem.get_attribute("data-platform")
                        current_dltype = dltype_elem.get_attribute("data-type")
                        current_platform_dltype_combo = (
                            f"{current_platform}_{current_dltype}"
                        )

                        # Get game, platform, dl_link
                        rows = wrapper_elem.find_elements(By.CLASS_NAME, "row")
                        print("for row in rows")
                        for row in rows:
                            title = row.find_element(By.CLASS_NAME, "title").text
                            print(f"{title=}")
                            subtitle = row.find_element(By.CLASS_NAME, "subtitle").text
                            print(f"{subtitle=}")

                            download = row.find_element(
                                By.CLASS_NAME, "js-start-download"
                            )
                            download_href = download.find_element(
                                By.TAG_NAME, "a"
                            ).get_attribute("href")
                            print(f"{download_href=}")

                            if title not in temp_dict.keys():
                                print(f"adding {title} to temp_dict")
                                temp_dict[title] = {}
                                temp_dict[title]["title"] = title
                                temp_dict[title]["subtitle"] = subtitle

                            if "drm_free_links" not in temp_dict[title]:
                                temp_dict[title]["drm_free_links"] = {}
                            temp_dict[title]["drm_free_links"][
                                current_platform_dltype_combo
                            ] = download_href

                            if (
                                current_platform
                                not in temp_dict[title]["drm_free_links"]
                            ):
                                temp_dict[title]["drm_free_links"][
                                    current_platform
                                ] = {}
                            temp_dict[title]["drm_free_links"][current_platform][
                                current_dltype
                            ] = download_href

                            temp_dict[title]["humble_bundle_page_link"] = url

                            print(f"tempdict for {title}")
                            pprint(temp_dict[title])

                wrapper_dict = temp_dict

                print("wrapper dict values")
                pprint(wrapper_dict.values(), indent=2)

                result.extend(wrapper_dict.values())

        return result


if __name__ == "__main__":
    hb = HumbleBundle()
    hb.login()
    hb.get_orders()
