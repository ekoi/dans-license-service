import uvicorn
from fastapi import FastAPI, Query
from typing import Union
import importlib.metadata

__version__ = importlib.metadata.metadata("dans-license-service")["version"]

app = FastAPI(title="DANS License Service", version=__version__)


@app.get('/')
def info():
    return {"version": __version__}


@app.get('/licenselibrary/license/{license_id}')
async def get_licence_by_id(license_id: str, format: Union[str] = Query(enum=["json-ld", "ttl", "rdf-xml"]), download: Union[bool] = Query(enum=[False, True])):
    return {}


@app.get('/licenselibrary/list')
async def get_license_list(keyword: str = Query(default=None), skip: int = Query(default=0), limit: int = Query(default=0)):
    return []

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=2004, reload=True)
