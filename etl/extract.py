import requests
from requests.auth import HTTPBasicAuth
from tenacity import retry, wait_exponential, stop_after_attempt


class ServiceNowExtractor:
    def __init__(self, instance, user, password, table, fields, page_size=1000):
        self.instance = instance.rstrip('/')
        self.user = user
        self.password = password
        self.table = table
        self.fields = fields
        self.page_size = page_size

    @retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
    def fetch(self, query=None, max_records=10000):
        """Generator that yields records from ServiceNow using the Table API"""
        offset = 0
        fetched = 0
        headers = {"Accept": "application/json"}
        while True:
            params = {
                'sysparm_limit': self.page_size,
                'sysparm_offset': offset,
                'sysparm_fields': ','.join(self.fields)
            }
            if query:
                params['sysparm_query'] = query

            url = f"{self.instance}/api/now/table/{self.table}"
            resp = requests.get(url, auth=HTTPBasicAuth(self.user, self.password), headers=headers, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            result = data.get('result', [])
            if not result:
                break
            for row in result:
                yield row
                fetched += 1
                if fetched >= max_records:
                    return
            offset += len(result)
