from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .recommend import recommend

app = FastAPI()

class RecommendRequest(BaseModel):
    request_id: int

@app.post("/recommend")
def get_recommendations(body: RecommendRequest):
    try:
        results = recommend(body.request_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    if results.empty:
        raise HTTPException(status_code=404, detail="No hospitals found")
    
    return results.to_dict(orient="records")

@app.get("/health")
def health():
    return {"status": "ok"}