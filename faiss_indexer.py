import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
index = None
id_map = []

# Turn text into vector
def embed_chunks(chunks):
    return model.encode(chunks, convert_to_numpy=True)

# Build index
def build_index(embeddings, ids):
    global index, id_map
    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    id_map = ids
    index.add(np.array(embeddings).astype("float32"))

# Search index and return MongoDB IDs
def search_index(query_vector, k=3):
    D, I = index.search(np.array([query_vector]).astype("float32"), k)
    return [id_map[i] for i in I[0] if i < len(id_map)]
