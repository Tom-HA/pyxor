import os
import logging
import uvicorn
from pydantic import BaseModel
from jsonpath_rw.lexer import JsonPathLexerError
from yaml import YAMLError
from fastapi import FastAPI, Response, status
from fastapi.encoders import jsonable_encoder
from internal import parser

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%(levelname)s:\t\t%(message)s')
app = FastAPI()

class Extraction(BaseModel):
    text: str
    expr: str
    
@app.get("/health")
def health_check():
    return {"alive": "true"}


@app.post("/api/yaml_extract")
def extract_yaml(extraction: Extraction, response: Response):
    try:
        r = parser.extract_values_from_yaml(extraction.text, extraction.expr)
    except YAMLError as e:
        logging.warning(e)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {"data": "Failed to parse YAML"}
    except JsonPathLexerError as e:
        logging.warning(e)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {"data": "Failed to parse YAML path expression"}
    except AttributeError as e:
        logging.warning(e)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {"data": "Failed to parse request"}
        
    except Exception as e:
        logging.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"data": "Unhandled exception"}
        
    resp = {"data": r}
    return resp
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
    

