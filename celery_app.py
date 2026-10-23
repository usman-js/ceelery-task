
from celery import Celery
from kombu import Exchange, Queue

app = Celery(
    "ecommerce",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
    include=["app.tasks"],
)

default_exchange = Exchange("default_queue", type="direct")
heavy_exchange = Exchange("heavy_media_queue", type="direct")

app.conf.update(
    task_queues=(
        Queue(
            "default_queue",
            exchange=default_exchange,
            routing_key="default_queue",
        ),
        Queue(
            "heavy_media_queue",
            exchange=heavy_exchange,
            routing_key="heavy_media_queue",
        ),
    ),
    task_default_queue="default_queue",
    task_default_exchange="default_queue",
    task_default_exchange_type="direct",
    task_default_routing_key="default_queue",
    task_routes={
        "app.tasks.simulate_network_request": {
            "queue": "default_queue",
            "routing_key": "default_queue",
        },
        "app.tasks.process_heavy_media": {
            "queue": "heavy_media_queue",
            "routing_key": "heavy_media_queue",
        },
    },
    task_track_started=True,
    task_send_sent_event=True,
    worker_send_task_events=True,
)
