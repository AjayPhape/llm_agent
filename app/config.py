import os

from langchain_community.llms.llamacpp import LlamaCpp
from langchain_ollama import OllamaEmbeddings
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    dbname: str = "simple_llm"
    user: str = ""
    password: str = ""
    host: str = "localhost"
    port: int = 5432

    class Config:
        env_file = ".env"  # Specify the .env file to load variables from
        env_file_encoding = "utf-8"


def get_embeddings():
    # from langchain_huggingface.embeddings import HuggingFaceEmbeddings
    # return HuggingFaceEmbeddings(
    #     model_name="sentence-transformers/all-MiniLM-L6-v2",
    #     model_kwargs={"device": "cpu"},
    # )
    return OllamaEmbeddings(model="nomic-embed-text")


def get_llm():
    return LlamaCpp(
        model_path=f"{os.path.expanduser('~')}/Downloads/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
        n_ctx=2300,
        n_gpu_layers=50,
        n_threads=12,
        verbose=False,
    )


llm = get_llm()

embedding = get_embeddings()

db_settings = DatabaseSettings()
