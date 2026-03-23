import os
from pathlib import Path
from dotenv import load_dotenv
import yaml

BASE_DIR = Path(__file__).resolve().parents[1]

load_dotenv(BASE_DIR / '.env')

class Config:
    def __init__(self, config_path=BASE_DIR / 'config.yaml'):
        with open(config_path, 'r') as f:
            self._raw = yaml.safe_load(f)

    @property
    def servicenow(self):
        return {
            'instance': os.getenv('SERVICENOW_INSTANCE'),
            'user': os.getenv('SERVICENOW_USER'),
            'password': os.getenv('SERVICENOW_PASSWORD'),
            'table': self._raw.get('servicenow', {}).get('table'),
            'fields': self._raw.get('servicenow', {}).get('fields', [])
        }

    @property
    def sql(self):
        return {
            'driver': os.getenv('SQLSERVER_DRIVER'),
            'server': os.getenv('SQLSERVER_SERVER'),
            'database': os.getenv('SQLSERVER_DATABASE'),
            'user': os.getenv('SQLSERVER_USER'),
            'password': os.getenv('SQLSERVER_PASSWORD'),
            'table': self._raw.get('sql', {}).get('table'),
            'upsert_key': self._raw.get('sql', {}).get('upsert_key'),
            'columns': self._raw.get('sql', {}).get('columns', {})
        }

    @property
    def fetch(self):
        page_size = int(os.getenv('PAGE_SIZE', self._raw.get('fetch', {}).get('page_size', 1000)))
        max_records = int(self._raw.get('fetch', {}).get('max_records', 10000))
        return {'page_size': page_size, 'max_records': max_records}
