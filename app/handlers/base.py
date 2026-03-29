from nats.js.api import (
    ConsumerConfig,
    DeliverPolicy,
    AckPolicy
)

base_consumer_config = ConsumerConfig(
    deliver_policy=DeliverPolicy.ALL,
    ack_policy=AckPolicy.EXPLICIT,
    max_deliver=4,
    backoff=[10.0, 20.0, 30.0],
)
