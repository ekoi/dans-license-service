import json
import os
from rdflib import Graph

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status, Query, Request
from fastapi.security import OAuth2PasswordBearer
from typing import Union
import importlib.metadata
import logging
__version__ = importlib.metadata.metadata("dans-license-service")["version"]

from dynaconf import Dynaconf

settings = Dynaconf(settings_files=["conf/settings.toml", "conf/.secrets.toml"],
                    environments=True)

logging.basicConfig(filename=settings.LOG_FILE, level=settings.LOG_LEVEL,
                    format=settings.LOG_FORMAT)

data = {}

api_keys = [
    settings.DANS_LICENSE_SERVICE_API_KEY
]  # Todo: This is encrypted in the .secrets.toml

#Authorization Form: It doesn't matter what you type in the form, it won't work yet. But we'll get there.
#See: https://fastapi.tiangolo.com/tutorial/security/first-steps/
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # use token authentication



def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    if api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )


app = FastAPI(title=settings.FASTAPI_TITLE, description=settings.FASTAPI_DESCRIPTION,
              version=__version__)


def iterate_saved_license_dir():
    for filename in os.listdir(settings.LICENCES_DIR):
        if filename.startswith("licence_") and filename.endswith(".json"):
            logging.debug(filename)  # logging.debuging file name of desired extension
            with open (os.path.join(settings.LICENCES_DIR, filename), "r") as f:
                f_json = json.load(f)
                data.update({f_json["@id"]:f_json})
        else:
            continue

@app.on_event('startup')
def read_licenses():
    logging.debug("startup")
    iterate_saved_license_dir()
    with open(settings.LICENCES_LIST_FILE) as f:
        f_json = json.load(f)
        data.update({"license": f_json["license"]})
    return data

@app.get('/', tags=["public"])
def info():
    return {"version": __version__}


@app.get('/licenselibrary/license/{license_id}', tags=["public"])
async def get_licence_by_id(license_id: str, format: Union[str] = Query(enum=["json-ld", "ttl", "rdf-xml"]), download: Union[bool] = Query(enum=[False, True])):
    license = data.get(license_id)
    if license :
        g = Graph().parse(data=license, format='json-ld')
        if format == "rdf-xml":
            result = g.serialize(format="pretty-xml")
        elif format == "ttl":
            result = g.serialize(format="ttl")
        else:
            result = g.serialize(format="json-ld")
        return result
    return {}


@app.get('/licenselibrary/list', tags=["public"])
async def get_license_list(keyword: str = Query(default=None), skip: int = Query(default=0), limit: int = Query(default=0)):
    return data.get("license")

@app.post('/add-license', tags=["protected"], dependencies=[Depends(api_key_auth)])
async def add_license(submitted_license: Request):
    raise HTTPException(status_code=501, detail=f'This endpoint is not implemented yet.')


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=33163, reload=True)
