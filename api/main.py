import uvicorn
from fastapi import APIRouter, FastAPI

from api.views import router

app = FastAPI(docs_url="/docs")

app.include_router(router)
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=5008)
