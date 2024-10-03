from typing import override

from onepassword.types import Item
from secrecy.abc.asyncio import SecretsSource


class OnePasswordSdkSecretsSource(SecretsSource):
    def __init__(self, client, vault_id: str, item_id: str) -> None:
        super().__init__()
        self.client = client
        self.vault_id = vault_id
        self.item_id = item_id

    @override
    async def pull(self) -> dict[str, str]:
        secret: Item = await self.client.items.get(self.vault_id, self.item_id)

        secrets: dict[str, str] = {}
        for field in secret.fields:
            secrets[field.title] = str(field.value)

        return secrets

    @override
    async def push(self, values: dict[str, str]) -> None:
        raise NotImplementedError()
