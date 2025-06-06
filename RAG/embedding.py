import os
import json

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

from vectorizer import mapping
from extractor import parts
from vectorizer.ingestor import ingest_terms, ingest_abbreviations, ingest_items


load_dotenv()  # take environment variables from .env.

# --- Configuration ---
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")
ELASTICSEARCH_API_KEY = os.getenv("ELASTICSEARCH_API_KEY")

# Initialize Elasticsearch client
es_client = Elasticsearch(ELASTICSEARCH_URL, api_key=ELASTICSEARCH_API_KEY)

# --- Helper function to create index if it doesn't exist ---
def create_index_if_not_exists(es_client, index_name, mapping):
    if not es_client.indices.exists(index=index_name):
        try:
            es_client.indices.create(index=index_name, body=mapping)
            print(f"Index '{index_name}' created successfully.")
        except Exception as e:
            print(f"Error creating index '{index_name}': {e}")
    else:
        print(f"Index '{index_name}' already exists.")

# Create indices
create_index_if_not_exists(es_client, mapping.terms_index_name, mapping.terms_mapping)
create_index_if_not_exists(es_client, mapping.abbreviations_index_name, mapping.abbreviations_mapping)
create_index_if_not_exists(es_client, mapping.items_index_name, mapping.items_mapping)


# --- Load your JSON data (replace with your actual data loading) ---
dir_path = f'{os.path.dirname(os.path.realpath(__file__))}/parsed/'
with open(f'{dir_path}{parts[0]['file']}.json', 'r') as f:
  terms_data = json.load(f)
with open(f'{dir_path}{parts[1]['file']}.json', 'r') as f:
  abbreviations_data = json.load(f)
with open(f'{dir_path}{parts[2]['file']}.json', 'r') as f:
  items_data = json.load(f)
  
  
# with open('_1_terms_14_32', 'r') as f:
#   terms_data = json.load(f)
# with open('_2_acronyms_and_abbreviations_33_36', 'r') as f:
#   abbreviations_data = json.load(f)
# with open('_3_category_9_aerospace_and_propulsion_286_308', 'r') as f:
#   items_data = json.load(f)


# Run ingestion
print("\n--- Starting Ingestion ---")
ingest_terms(es_client, terms_data, mapping.terms_index_name, mapping.embedding_model)
ingest_abbreviations(es_client, abbreviations_data, mapping.abbreviations_index_name, mapping.embedding_model)
ingest_items(es_client, items_data, mapping.items_index_name, mapping.embedding_model)

print("\n--- Ingestion Complete ---")

user_query = "What are active flight control systems?"
query_embedding = mapping.embedding_model.encode(user_query)