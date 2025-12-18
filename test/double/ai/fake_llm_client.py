class FakeLLMClient:
    async def generate(self, messages: list[dict[str, str]]) -> str:
        return "This is a fake response from FakeClient."
