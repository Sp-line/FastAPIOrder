from nats.js.api import (
    ConsumerConfig,
    DeliverPolicy,
    AckPolicy
)

base_consumer_config = ConsumerConfig(
    deliver_policy=DeliverPolicy.ALL,
    ack_policy=AckPolicy.EXPLICIT,
    max_deliver=3,
    ack_wait=10.0,
)
