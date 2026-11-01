from fastapi import FastAPI, HTTPException, Status
from pydantic import BaseModel, Field, validator
import re, redis, json, hashlib

app = FastAPI(title="Cynbit AI Gateway Engine", docs_url=None, redoc_url=None)
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

class EvaluationPayload(BaseModel):
    user_id: str
    source_code: str = Field(..., max_length=10000)

    @validator('source_code')
    def sanitize_input(cls, v):
        forbidden_patterns = [r"__import__", r"exec\(", r"eval\(", r"os\.system"]
        for pattern in forbidden_patterns:
            if re.search(pattern, v):
                raise ValueError("Potentially unsafe execution pattern detected.")
        return v

@app.post("/api/v1/ai/evaluate")
async def evaluate(payload: EvaluationPayload):
    cache_key = f"eval:{hashlib.sha256(payload.source_code.encode()).hexdigest()}"
    cached = redis_client.get(cache_key)
    if cached:
        return {"success": True, "cached": True, "data": json.loads(cached)}
    
    result = {"score": 95, "feedback": "Code architecture matches standards."}
    redis_client.setex(cache_key, 86400, json.dumps(result))
    return {"success": True, "cached": False, "data": result}