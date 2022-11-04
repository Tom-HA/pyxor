import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from internal import parser

app = FastAPI()

class Extraction(BaseModel):
    text: str
    expr: str
    
@app.get("/health")
def health_check():
    return {"alive": "true"}


@app.post("/api/yaml_extract")
def extract_yaml(extraction: Extraction):
    try:
        r = parser.extract_values_from_yaml(extraction.text, extraction.expr)
        resp = {"data": r}
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
    

