

import requests
from pprint import pprint
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = 'https://www.humblebundle.com'
LOGIN = 'https://www.humblebundle.com/login'
PROCESS_LOGIN = 'https://www.humblebundle.com/processlogin'
ORDERS = 'https://www.humblebundle.com/api/v1/user/order'
ORDERS_DETAILS = 'https://www.humblebundle.com/api/v1/orders?all_tpkds=true&gamekeys=Pd3yaUzfUEe2Xzhf&gamekeys=hn2uW8Kpe4XT75Dz&gamekeys=76vhyUqM4y6nwRby&gamekeys=VseEKV5thcc8577m&gamekeys=tpruBqvqvaFtWkPA&gamekeys=Y3F3qfauqaF6kA8A&gamekeys=466EA5A6Rx4yNH4u&gamekeys=wHMYGsT74q8dbBE2&gamekeys=M2wZZvUPV7y853YS&gamekeys=yU6FNfNVMMuV8Ztx&gamekeys=rxhVtaAqXPddrYFz&gamekeys=bm5YUAabtrFHbPN3&gamekeys=AnN4xCFWqfGPx3WF&gamekeys=cfHRSdyxsBFPftFA&gamekeys=uz62zHmSumhGvNss&gamekeys=b6pkxyK8kMaEuU7p&gamekeys=q7VtwRqfcDKV3kNT&gamekeys=yPHwurnGswNMycMb&gamekeys=ckGpnppx4B7V7wA3&gamekeys=tzDdrsHketVWRz7F&gamekeys=nyvyYV7r2WFP8KpY&gamekeys=fTRzUu2u2UyrwDC3&gamekeys=DsFHz8Mt4xPDfvyK&gamekeys=yfsnceXp6spaaxBD&gamekeys=Ws6RB4UyMFm2zva5&gamekeys=Ar2G6UqVEAF72mT3&gamekeys=cqsaZBrkazFV8aTC&gamekeys=S6nVrEZSWwY7Hs8U&gamekeys=a3mRA4DuVdqNMZPm&gamekeys=RW8ZVwpc4PAF8cWC&gamekeys=Xtz6zbXbvhCKRNZv&gamekeys=hz6XvvqPdBSeqESV&gamekeys=yupENF4Ba4RhwEDc&gamekeys=dZz82yvqedDhFxAq&gamekeys=H4PyBrDs4NzKV38S&gamekeys=2u8rHD6dVXMxS5F4&gamekeys=GBbVxaaFeXFw3XnE&gamekeys=2fGxTqkymsDpDMbP&gamekeys=vFrf7uppMc7cvuRc&gamekeys=fXn8vevpkpDH2CHp'
PURCHASES = 'https://www.humblebundle.com/home/purchases'

class HumbleBundle():
    def __init__(self):
        self.session = requests.Session()
        self.session.get(BASE_URL)
        
        print('cookies')
        pprint(self.session.cookies)

    def login(self):
        USERNAME = os.getenv('USERNAME')
        PASSWORD = os.getenv('PASSWORD')

        form_data = {
            "access_token": "",
            "access_token_provider_id": "",
            "goto": "/",
            "qs": "",
            "username": USERNAME,
            "password": PASSWORD
        }

        res = self.session.post(PROCESS_LOGIN, json=form_data)
        
        print(res)
        print(res.status_code)

        pprint(res.text)

        try:
            pprint(res.json())
        except Exception as e:
            print('Exception', e)

        

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



if __name__ == '__main__':
    hb = HumbleBundle()
    hb.login()
    # hb.get_purchases()

