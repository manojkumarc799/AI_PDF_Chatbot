import faiss
import numpy as np


def create_vector_store(embeddings):
    """
    Create a FAISS index from embeddings.
    """

    embeddings = np.asarray(embeddings, dtype="float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index


def search_vector_store(index, query_embedding, top_k=3):
    """
    Search the FAISS index and return the closest chunks.
    """

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    query_embedding = query_embedding.reshape(1, -1)

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    return distances[0], indices[0]