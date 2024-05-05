import json

from fastapi import FastAPI, APIRouter, Request
from app.services import openai_service, pinecone_service, scraping_service
from app.utils.helper_functions import chunk_text, build_prompt, construct_messages_list
import pickle
import requests

app = FastAPI(title="RAG-LLM-app")
router = APIRouter()

PINECONE_INDEX_NAME = "rag-llm-app"

@router.post('/embed-and-store')
def embed_and_store():
    with open('_books.pickle', 'rb') as f:
        books = pickle.load(f)
    with open('embeds.pickle', 'rb') as f:
        embeds = pickle.load(f)
    pinecone_service.embed_chunks_and_upload_to_pinecone(books, embeds, PINECONE_INDEX_NAME)
    response_json = {
        "message": "Chunks embedded and stored successfully"
    }
    return response_json


@router.post('/handle-query')
async def handle_query(question):
    recs = pinecone_service.get_most_similar_chunks_for_query(question, PINECONE_INDEX_NAME)
    prompt = build_prompt(question, recs)
    #messages = construct_messages_list(chat_history, prompt)
    answer = openai_service.get_llm_answer(prompt)
    return answer  


@router.post('/delete-index')
def delete_index():
    pinecone_service.delete_index()
    return {"message": f"Indexes deleted successfully"}

app.include_router(router)

if __name__ == "__main__":
    import uvicorn  # pylint: disable=import-outside-toplevel
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        workers=1,
        use_colors=True,
    )