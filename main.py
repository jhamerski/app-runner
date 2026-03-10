from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Olá do App Runner!"}
