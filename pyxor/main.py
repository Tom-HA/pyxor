import os
import logging
import uvicorn
from pydantic import BaseModel
from jsonpath_rw.lexer import JsonPathLexerError
from yaml import YAMLError
from fastapi import FastAPI, Response, status, Request
from internal import parser
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%(levelname)s:\t\t%(message)s')
app = FastAPI()

class ExtractionRequest(BaseModel):
    text: str
    expr: str

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"data": "Invalid request"}),
    )

@app.get("/health")
def health_check():
    return {"alive": "true"}


@app.post("/api/yaml_extract")
def extract_yaml(extraction: ExtractionRequest, response: Response):
    try:
        resp = parser.extract_values_from_yaml(extraction.text, extraction.expr)
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
        
    return resp
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
    

