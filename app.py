import uvicorn
from google.adk.cli.fast_api import get_fast_api_app

app = get_fast_api_app(web=True, agents_dir=".")
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
