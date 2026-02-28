import string

from nanoid import generate  # type: ignore[import-untyped]

from constants import OrderLimits


def generate_order_public_code() -> str:
    return generate(alphabet=OrderLimits.PUBLIC_CODE_ALPHABET, size=OrderLimits.PUBLIC_CODE_MAX)