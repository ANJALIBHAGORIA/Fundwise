"""
ingestion_scheduler.py
---------------------
Purpose:
    Schedule periodic ingestion of UPI transactions and user events
    to ensure data pipelines are up-to-date.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from upi_webhook_ingestor import UPIWebhookIngestor
from user_event_ingestor import UserEventIngestor

class IngestionScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def schedule_ingestion(self, interval_seconds: int, function, *args, **kwargs):
        self.scheduler.add_job(function, 'interval', seconds=interval_seconds, args=args, kwargs=kwargs)
        self.scheduler.start()
        print(f"Ingestion job scheduled every {interval_seconds} seconds for {function.__name__}")

if __name__ == "__main__":
    upi_ingestor = UPIWebhookIngestor('transactions.csv')
    user_ingestor = UserEventIngestor('user_events.csv')

    scheduler = IngestionScheduler()
    scheduler.schedule_ingestion(30, upi_ingestor.ingest_webhook, {'txn_id':'TXN999','user_id':102,'fund_id':202,'amount':300,'status':'SUCCESS'})
    scheduler.schedule_ingestion(60, user_ingestor.ingest_event, 102, 'login', {'ip':'10.0.0.1'})
