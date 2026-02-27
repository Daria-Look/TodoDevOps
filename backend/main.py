from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "DevOps"}

@app.get("/health")
def health():
    return {"status": "ok"}
