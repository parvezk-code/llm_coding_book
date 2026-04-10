

class BaseEmbeddingModel:

    def load_model(self):
        pass

    def generate_embeddings(self, texts):
        pass

    def generate_query_embedding(self, query):
        pass




class SentenceTransformerModel(BaseEmbeddingModel):

    def load_model(self):
        self.model = SentenceTransformer(self.model_name)

    def generate_embeddings(self, texts):
        return self.model.encode(texts)

    def generate_query_embedding(self, query):
        return self.model.encode([query])[0]



class OpenAIEmbeddingModel(BaseEmbeddingModel):

    def load_model(self):
        self.client = OpenAI()

    def generate_embeddings(self, texts):
        return client.embeddings.create(input=texts)

    def generate_query_embedding(self, query):
        return client.embeddings.create(input=[query])[0]