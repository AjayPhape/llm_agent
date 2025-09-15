import logging

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

from simple_llm.app.config import embedding, llm
from simple_llm.app.pg_db import DatabaseConnection

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def build_inputs(q: str) -> dict:
    with DatabaseConnection() as conn:
        qry = """
            WITH tmp AS (
                SELECT
                    content,
                    jsonb_build_object('rec_id', id) || metadata as metadata
                FROM
                    book
                ORDER BY
                    embedding <-> %(query_embedding)s::vector
                LIMIT %(k)s
            )
            SELECT 
                string_agg(content, '\\n\\n') AS aggregated_content,
                jsonb_agg(metadata) AS aggregated_metadata
            FROM
                tmp;
        """
        params = {"k": 6, "query_embedding": embedding.embed_query(q)}
        ctx, docs = conn.fetchone(qry, params)
    return {"qry": q, "ctx": ctx.strip(), "docs": docs}


# 5
prompt = PromptTemplate(
    input_variables=["ctx", "qry"],
    template="Use the following context to answer the question.\n\nContext: {ctx}\n\nQuestion: {qry}\n\nAnswer:",
)

#  6
# rag_chain = (
#     {"ctx": lambda q: format_from_source(retriever.invoke(q)), "qry": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )

rag_source_chain = RunnableLambda(build_inputs) | {
    "answer": (
        (lambda x: {"qry": x["qry"], "ctx": x["ctx"]})
        | prompt
        | llm
        | StrOutputParser()
    ),
    "source": lambda x: x["docs"],
}
