from typing import Dict, List


class FakeClient:
    async def generate(self, messages: List[Dict[str, str]]) -> str:
        return "This is a fake response from FakeClient."
