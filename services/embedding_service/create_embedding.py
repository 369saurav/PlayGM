from sentence_transformers import SentenceTransformer

# model = SentenceTransformer('all-MiniLM-L6-v2')
model = SentenceTransformer('all-mpnet-base-v2')


def get_embedding(data):
    embedding = model.encode(data)
    return embedding