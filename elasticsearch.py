from RAG.vectorizer.mapping import embedding_model

user_query = "What are active flight control systems?"
query_embedding = embedding_model.encode(user_query)