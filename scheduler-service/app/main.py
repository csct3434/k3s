from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "스케줄러 : 이제 되는거 같다~~~"}
