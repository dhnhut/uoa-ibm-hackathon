
from sentence_transformers import SentenceTransformer

# Load a pre-trained model
model_name = 'msmarco-distilbert-base-v4' # 768 dimensions
embedding_model = SentenceTransformer(model_name)
embedding_dim = embedding_model.get_sentence_embedding_dimension()
print(f"Using embedding model: {model_name} with dimension: {embedding_dim}")

terms_index_name = "rag_terms"
terms_mapping = {
    "mappings": {
        "properties": {
            "term_text": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "definition_text": {"type": "text"},
            "categories_keyword": {"type": "keyword"}, # For filtering
            "combined_text_for_embedding": {"type": "text", "index": False}, # Store for reference, not directly searched
            "embedding": {"type": "dense_vector", "dims": embedding_dim, "index": True, "similarity": "cosine"}
        }
    }
}

abbreviations_index_name = "rag_abbreviations"
abbreviations_mapping = {
    "mappings": {
        "properties": {
            "acronym_text": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "meaning_text": {"type": "text"},
            "combined_text_for_embedding": {"type": "text", "index": False},
            "embedding": {"type": "dense_vector", "dims": embedding_dim, "index": True, "similarity": "cosine"}
        }
    }
}

items_index_name = "rag_items"
items_mapping = {
    "mappings": {
        "properties": {
            "item_id_keyword": {"type": "keyword"},
            "description_text": {"type": "text"}, # This will be used for embedding
            "embedding": {"type": "dense_vector", "dims": embedding_dim, "index": True, "similarity": "cosine"}
        }
    }
}