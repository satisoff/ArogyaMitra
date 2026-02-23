from fastapi import FastAPI

app = FastAPI(title="ArogyaMitra AI Wellness API")

@app.get("/")
def root():
    return {"message": "ArogyaMitra backend running"}