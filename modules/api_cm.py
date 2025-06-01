import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
import os

BASE_URL = os.getenv('CM_API_URL', '')
CM_API_KEY = os.getenv('CM_API_KEY', '')

HEALTH_URL = f"{BASE_URL}health"
ADD_CAR_URL = f"{BASE_URL}parser/add_new_car"

HEADERS = {
    'accept': 'application/json',
    'X-API-KEY': CM_API_KEY
}

response = requests.get(HEALTH_URL, headers=HEADERS, verify=False)


def get_cm_health():
    try:
        if response.status_code == 200:
            data = response.json()
            return all(
                info.get('status') == 1
                for module, info in data.items()
                if module != "voperator_module"
            )
        return False
    except Exception as e:
        print(f"Ошибка при проверке статуса: {e}")
        return False