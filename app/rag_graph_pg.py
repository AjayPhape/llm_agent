import logging
from typing import TypedDict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph
from simple_llm.app.config import embedding, llm
from simple_llm.app.pg_db import DatabaseConnection

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


class State(TypedDict):
    prompt: str
    answer: str
    source: list
    context: str
    next_state: str


def start(state: State) -> dict:
    logger.info("started the workflow")
    return state


def retrieve_source(state: State) -> dict:
    q = state["prompt"]
    with DatabaseConnection() as conn:
        qry = """
            WITH var AS (
                SELECT %(query_embedding)s::vector as input_vector
            ),
            tmp AS (
                select
                    content,
                    jsonb_build_object('rec_id', id) || metadata as metadata,
                    embedding <-> input_vector as distance
                from
                    book
                CROSS JOIN var
                where
                    embedding <-> input_vector < 0.87
                order by
                    distance
                LIMIT %(k)s
            )
            SELECT 
                string_agg(content, '\\n\\n') AS aggregated_content,
                jsonb_agg(metadata) AS aggregated_metadata
            FROM
                tmp;
        """
        params = {"k": 6, "query_embedding": embedding.embed_query(q)}
        ctx, source = conn.fetchone(qry, params)
        state.update({"context": ctx and ctx.strip(), "source": source or []})
    return state


# 5
rag_prompt = PromptTemplate(
    input_variables=["ctx", "qry"],
    template="Use the following context to answer the question.\n\nContext: {ctx}\n\nQuestion: {qry}\n\nAnswer:",
)

normal_prompt = PromptTemplate(
    input_variables=["qry"],
    template="You are a helpful assistant. Answer the following question:\n\nQuestion: {qry}\n\nAnswer:",
)


def decide(state: State) -> str:
    return "RAG" if state["source"] else "NORMAL"


def run_chain(state: State, prompt: PromptTemplate):
    chain = (
        (lambda x: {"qry": state["prompt"], "ctx": state.get("context", "")})
        | prompt
        | llm
        | StrOutputParser()
    )
    state["answer"] = chain.invoke({})
    return state


def rag_func(state: State):
    logger.info(f"Found {len(state['source'])} Doc(s) performing RAG")
    return run_chain(state, rag_prompt)


def normal_func(state: State):
    logger.info("Perform Normal Prompt")
    return run_chain(state, normal_prompt)


def out(state: State):
    logger.info(f"Output {state['answer']} source {state['source']}")


workflow = StateGraph(State)

workflow.add_node("start", start)
workflow.add_node("retrieve_source", retrieve_source)
workflow.add_node("rag_func", rag_func)
workflow.add_node("normal_func", normal_func)
workflow.add_node("output", out)

workflow.set_entry_point("start")
workflow.add_edge("start", "retrieve_source")
workflow.add_conditional_edges(
    "retrieve_source", decide, {"RAG": "rag_func", "NORMAL": "normal_func"}
)
workflow.add_edge("rag_func", "output")
workflow.add_edge("normal_func", "output")

workflow.set_finish_point("output")

llm_app = workflow.compile()


# result = llm_app.invoke({'prompt': input('Enter Prompt')})
