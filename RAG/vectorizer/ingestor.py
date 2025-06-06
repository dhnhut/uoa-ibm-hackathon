
from elasticsearch.helpers import bulk

# --- Process and Ingest Terms ---
def ingest_terms(es_client, data, index_name, model):
    actions = []
    texts_to_embed = []
    original_docs = []

    for i, doc in enumerate(data):
        # Clean the term: remove surrounding quotes if they are formatting artifacts
        clean_term = doc["term"].strip('“"”')
        text_for_embedding = f"{clean_term}: {doc['definition']}"
        texts_to_embed.append(text_for_embedding)
        original_docs.append({
            "_id": f"term_{i}", # Generate a unique ID
            "term_text": clean_term,
            "definition_text": doc["definition"],
            "categories_keyword": doc["categories"],
            "combined_text_for_embedding": text_for_embedding
        })

    if texts_to_embed:
        print(f"Generating embeddings for {len(texts_to_embed)} terms...")
        embeddings = model.encode(texts_to_embed, show_progress_bar=True)
        for orig_doc, emb in zip(original_docs, embeddings):
            action = {
                "_index": index_name,
                "_id": orig_doc.pop("_id"), # Use the generated ID
                "_source": {**orig_doc, "embedding": emb.tolist()}
            }
            actions.append(action)
        
        if actions:
            print(f"Bulk indexing {len(actions)} documents into '{index_name}'...")
            bulk(es_client, actions)
            print(f"Finished indexing terms.")

# --- Process and Ingest Abbreviations ---
def ingest_abbreviations(es_client, data, index_name, model):
    actions = []
    texts_to_embed = []
    original_docs = []

    for i, doc in enumerate(data):
        text_for_embedding = f"{doc['acronym']}: {doc['meaning']}"
        texts_to_embed.append(text_for_embedding)
        original_docs.append({
            "_id": f"abbr_{i}",
            "acronym_text": doc["acronym"],
            "meaning_text": doc["meaning"],
            "combined_text_for_embedding": text_for_embedding
        })
    
    if texts_to_embed:
        print(f"Generating embeddings for {len(texts_to_embed)} abbreviations...")
        embeddings = model.encode(texts_to_embed, show_progress_bar=True)
        for orig_doc, emb in zip(original_docs, embeddings):
            action = {
                "_index": index_name,
                "_id": orig_doc.pop("_id"),
                "_source": {**orig_doc, "embedding": emb.tolist()}
            }
            actions.append(action)

        if actions:
            print(f"Bulk indexing {len(actions)} documents into '{index_name}'...")
            bulk(es_client, actions)
            print(f"Finished indexing abbreviations.")

# --- Process and Ingest Items ---
# For items, the description can be long. Consider chunking for more granular retrieval.
# For simplicity here, we'll embed the whole description.
def ingest_items(es_client, data, index_name, model):
    actions = []
    texts_to_embed = [doc["description"] for doc in data if doc.get("description")] # Ensure description exists
    original_ids = [doc["id"] for doc in data if doc.get("description")]

    if texts_to_embed:
        print(f"Generating embeddings for {len(texts_to_embed)} items...")
        embeddings = model.encode(texts_to_embed, show_progress_bar=True)
        
        for item_id, description, emb in zip(original_ids, texts_to_embed, embeddings):
            action = {
                "_index": index_name,
                "_id": item_id, # Use the item's 'id' as the document ID
                "_source": {
                    "item_id_keyword": item_id,
                    "description_text": description,
                    "embedding": emb.tolist()
                }
            }
            actions.append(action)

        if actions:
            print(f"Bulk indexing {len(actions)} documents into '{index_name}'...")
            bulk(es_client, actions)
            print(f"Finished indexing items.")