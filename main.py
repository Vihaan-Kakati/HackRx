from fastapi import FastAPI, UploadFile, File, Form
from chunker import extract_chunks
from db import store_chunks, get_chunks_by_ids
from faiss_indexer import embed_chunks, build_index, search_index
from reasoner import ask_llm

app = FastAPI()

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    chunks = extract_chunks(contents)
    embeddings = embed_chunks(chunks)
    ids = store_chunks(chunks, embeddings)
    build_index(embeddings, ids)
    return {"message": "Document indexed.", "chunks": len(chunks)}

@app.post("/query")
async def query_document(question: str = Form(...)):
    query_embedding = embed_chunks([question])[0]
    top_ids = search_index(query_embedding)
    results = get_chunks_by_ids(top_ids)
    answer = ask_llm(question, results)  # Use LLM for final decision
    return {"results": results, "llm_response": answer}