from typing import Protocol


class UserAdapterProtocol(Protocol):
    def get(self) -> None: ...


class UserAdapter(UserAdapterProtocol):
    def __init__(self, session: str) -> None:
        self.session = session

    def get(self) -> None:
        print("User adapter get called")


class ItemAdapterProtocol(Protocol):
    def get(self) -> None: ...


class ItemAdapter(ItemAdapterProtocol):
    def __init__(self, client: str) -> None:
        self.client = client

    def get(self) -> None:
        print("Item adapter get called")
