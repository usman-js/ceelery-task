
import random

from celery_app import app


class NetworkFailureError(Exception):
    pass


@app.task(
    bind=True,
    autoretry_for=(NetworkFailureError,),
    retry_backoff=True,
    retry_backoff_max=60,
    retry_jitter=True,
    max_retries=4,
)
def simulate_network_request(self):
    print(f"Attempt {self.request.retries + 1}: contacting external service")

    if random.random() < 0.5:
        raise NetworkFailureError("Simulated intermittent network failure")

    return "Network request completed successfully"

import time


@app.task
def process_heavy_media():
    print("Starting heavy media processing...")
    time.sleep(10)
    print("Heavy media processing completed.")
    return "Media processing successful"
