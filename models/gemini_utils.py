import google.generativeai as genai
import numpy as np

class GeminiEmbedder:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.embed_content

    def get_embedding(self, text: str) -> np.ndarray:
        response = self.model(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_document"
        )
        return np.array(response['embedding'])
