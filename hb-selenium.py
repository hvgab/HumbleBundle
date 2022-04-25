

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

        wait = WebDriverWait(self.driver, 3000)

        print('Hide redeemed keys')
        # click to hide redeemed keys
        hide_redeemed = "xpath=//label[contains(.,'Hide redeemed keys & entitlements')]"
        wait.until(EC.presence_of_element_located((By.ID, 'hide-redeemed')))
        # self.driver.find_element(By.ID, "hide-redeemed").click()

        print('wait for table')
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'unredeemed-keys-table')))

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        self.driver.execute_script("window.scrollTo(0, 0)")

        self.driver.implicitly_wait(10)

        # Choices
        print('get choices')
        make_choices_urls_to_visit = []
        # elems = self.driver.find_elements(By.CLASS_NAME, 'choice-button')
        rows = self.driver.find_elements(By.CLASS_NAME, 'key-manager-choice-row')
        for row in rows:
            platform = row.find_element(By.CLASS_NAME, 'platform').text
            print('platform')
            print(platform)

            gamename_element = row.find_element(By.CLASS_NAME, 'game-name')
            gamename_title = gamename_element.find_element(By.TAG_NAME, 'h4').text
            print(f'{gamename_title=}')
            gamename_p = gamename_element.find_element(By.TAG_NAME, 'p').text
            print(f'{gamename_p=}')

            choice_url = row.find_element(By.CLASS_NAME, 'choice-button').get_attribute('href')
            print('choice_url')
            print(choice_url)

            make_choices_urls_to_visit.append({
                'platform': platform,
                'gamename': gamename,
                'choice_link': url,
            })
            
        pprint(make_choices_urls_to_visit)

        print('Getting next page')
            

        # elems = self.driver.find_elements(By.CLASS_NAME, 'key-manager-choice-row')
        # for elem in elems:
        #     print(elem.text)
        #     pprint(elem)
        #     elem.click
        #     sleep(10)



if __name__ == '__main__':
    hb = HumbleBundle()
    hb.login()
    hb.get_keys()

