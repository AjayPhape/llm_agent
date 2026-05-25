import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from simple_llm.app.rag_app_pg import rag_source_chain
from simple_llm.app.rag_graph_pg import llm_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
app = FastAPI()


class QueryRequest(BaseModel):
    prompt: str


class QueryResponse(BaseModel):
    answer: str
    sources: list


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    try:
        # Validate the input
        if not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

        # Invoke the RAG chain
        result = rag_source_chain.invoke(request.prompt)

        # Prepare the response
        logger.info(f"Result {result}")
        response = QueryResponse(
            answer=result.get("answer").strip(),
            sources=result.get("source", []),
        )
        return response

    except Exception as e:
        logger.exception(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")


@app.post("/graph_query", response_model=QueryResponse)
async def graph_query_endpoint(request: QueryRequest):
    try:
        # Validate the input
        if not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

        # Invoke the RAG chain
        result = llm_app.invoke({"prompt": request.prompt})

        # Prepare the response
        logger.info(f"Result {result}")
        response = QueryResponse(
            answer=result.get("answer").strip(),
            sources=result.get("source", []),
        )
        return response

    except Exception as e:
        logger.exception(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
