class BaseLLMClient:

    def generate(self, prompt: str) -> str:
        pass

    def generate_with_context(self, context: str, query: str) -> str:
        pass


class OpenAIClient(BaseLLMClient):

    def generate(self, prompt):
        response = client.chat.completions.create(...)
        return response