import logging
from etl.config import Config
from etl.extract import ServiceNowExtractor
from etl.transform import transform_records
from etl.load import SQLServerLoader


def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def run():
    setup_logging()
    cfg = Config()
    sn = cfg.servicenow
    sql = cfg.sql
    fetch = cfg.fetch

    extractor = ServiceNowExtractor(sn['instance'], sn['user'], sn['password'], sn['table'], sn['fields'], page_size=fetch['page_size'])
    loader = SQLServerLoader(sql['driver'], sql['server'], sql['database'], sql['user'], sql['password'], sql['table'])

    records = []
    for r in extractor.fetch(max_records=fetch['max_records']):
        records.append(r)

    if not records:
        logging.info('No records fetched')
        return

    df = transform_records(records, sql['columns'])

    inserted = loader.upsert_dataframe(df, sql['upsert_key'], sql['columns'])
    logging.info(f'Inserted {inserted} new rows')


if __name__ == '__main__':
    run()
