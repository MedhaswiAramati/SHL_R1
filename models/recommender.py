import pandas as pd
import numpy as np
from typing import List, Dict
from models.gemini_utils import GeminiEmbedder

class AssessmentRecommender:
    def __init__(self, api_key: str):
        self.api_key = api_key

        try:
            self.df = pd.read_csv("data/assessments.csv")
            print("CSV loaded. Columns:", self.df.columns)
        except FileNotFoundError:
            raise FileNotFoundError("CSV file not found at 'data/assessments.csv'")
        except Exception as e:
            raise Exception(f"Error loading CSV: {e}")

        if "Title" not in self.df.columns:
            raise KeyError("Column 'Title' not found in CSV.")

        self.embedder = GeminiEmbedder(api_key=self.api_key)

        # Generate embeddings for assessment titles
        try:
            self.df["embedding"] = self.df["Title"].apply(
                lambda title: self.embedder.get_embedding(str(title))
            )
        except Exception as e:
            raise Exception(f"Error generating embeddings: {e}")

    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def get_recommendations(self, query: str, top_k: int = 5) -> List[Dict]:
        query_embedding = self.embedder.get_embedding(query)

        self.df["similarity"] = self.df["embedding"].apply(
            lambda emb: self.cosine_similarity(emb, query_embedding)
        )

        top_results = self.df.sort_values(by="similarity", ascending=False).head(top_k)

        return [
            {
                "name": row.get("Title", "N/A"),
                "description": row.get("Description", "N/A"),
                "url": row.get("URL", "N/A")
            }
            for _, row in top_results.iterrows()
        ]
