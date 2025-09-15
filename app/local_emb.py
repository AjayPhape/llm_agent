from simple_llm.app.config import embedding

# from langchain_huggingface import HuggingFaceEmbeddings
# from transformers import AutoModel, AutoTokenizer


# model_id = "sentence-transformers/all-MiniLM-L6-v2"
# AutoModel.from_pretrained(model_id).save_pretrained("./local_emb_model")
# AutoTokenizer.from_pretrained(model_id).save_pretrained("./local_emb_model")


print(embedding.embed_query("Popular Hobbies"))
