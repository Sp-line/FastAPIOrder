from nats.js.api import (
    ConsumerConfig,
    DeliverPolicy,
    AckPolicy
)

from core.config import settings

base_consumer_config = ConsumerConfig(
    deliver_policy=settings.faststream.consumer.deliver_policy,
    ack_policy=settings.faststream.consumer.ack_policy,
    max_deliver=settings.faststream.consumer.max_deliver,
    backoff=settings.faststream.consumer.backoff,
)
