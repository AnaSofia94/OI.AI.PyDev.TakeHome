import uvicorn
from src.batch import app

if __name__ == "__main__":
    uvicorn.run("batch:app", host="127.0.0.1", port=8000, reload=True)