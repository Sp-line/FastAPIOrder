from dishka import Provider, Scope, provide

from domain.rules import EnsureOrderCanBeModified, EnsureSessionIsOpen, EnsureSeatValidForSession, \
    EnsureUserCanCreateOrder


class DomainProvider(Provider):
    scope = Scope.REQUEST

    get_ensure_order_can_be_modified = provide(EnsureOrderCanBeModified)
    get_ensure_seat_valid_for_session = provide(EnsureSeatValidForSession)
    get_ensure_user_can_create_order = provide(EnsureUserCanCreateOrder)

    @provide
    def get_ensure_session_is_open(self) -> EnsureSessionIsOpen:
        return EnsureSessionIsOpen()
