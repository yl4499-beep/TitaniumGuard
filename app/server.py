"""Thin same-origin API for TitaniumGuard; statistical work belongs in qc.py."""
from pathlib import Path
from typing import Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field, StrictInt
if __package__:
    from .qc import analyze_records, parse_csv
else:
    from qc import analyze_records, parse_csv

BASE=Path(__file__).resolve().parent
api=FastAPI(title='TitaniumGuard',version='1.0.0',docs_url=None,redoc_url=None,description='Frozen-baseline X-bar/R monitoring and strength capability. Synthetic demos; no part release certification.')
api.mount('/assets',StaticFiles(directory=BASE/'static'),name='assets')
DATASETS={'stable_capable':'Stable process','mean_shift':'Mean shift','stable_incapable':'Low margin'}
class AnalysisRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    csv_text: str|None=Field(default=None,strict=True,max_length=2_000_000)
    records: list[dict[str,Any]]|None=Field(default=None,max_length=20_000)
    lsl: float=Field(default=900,strict=True,allow_inf_nan=False,gt=0)
    usl: float|None=Field(default=None,strict=True,allow_inf_nan=False,gt=0)
    baseline_builds: StrictInt=Field(default=25,ge=2)
    target: float=Field(default=1.33,strict=True,allow_inf_nan=False,gt=0)

@api.exception_handler(RequestValidationError)
async def request_validation_error(request: Request, exc: RequestValidationError):
    # Do not echo raw inputs or error contexts: nonfinite input can otherwise
    # make JSON serialization fail and turn an actionable422 into a500.
    detail = [
        {'loc': list(error['loc']), 'msg': error['msg'], 'type': error['type']}
        for error in exc.errors()
    ]
    return JSONResponse(status_code=422, content={'detail': detail})

@api.get('/docs',include_in_schema=False)
def interactive_docs(request: Request):
    # Root path is supplied by a mounted app or the deployment proxy. Keep all
    # Swagger resources local so documentation works without a CDN connection.
    root_path = request.scope.get('root_path', '').rstrip('/')
    return get_swagger_ui_html(
        openapi_url=root_path + api.openapi_url,
        title='TitaniumGuard — API documentation',
        swagger_js_url=root_path + '/assets/vendor/swagger-ui-bundle.js',
        swagger_css_url=root_path + '/assets/vendor/swagger-ui.css',
        swagger_favicon_url='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22%3E%3Crect width=%2232%22 height=%2232%22 rx=%225%22 fill=%22%23102838%22/%3E%3Ctext x=%226%22 y=%2223%22 fill=%22white%22 font-size=%2220%22%3ETi%3C/text%3E%3C/svg%3E',
        swagger_ui_parameters={'validatorUrl': None},
    )

@api.get('/',include_in_schema=False)
def home():return FileResponse(BASE/'static'/'index.html')
@api.get('/health')
def health():return {'status':'ok','version':'1.0.0'}
@api.get('/api/datasets')
def datasets():return [{'id':k,'label':v,'synthetic':True} for k,v in DATASETS.items()]
@api.get('/api/datasets/{name}')
def dataset(name:str):
    if name not in DATASETS:raise HTTPException(404,'Unknown demonstration dataset.')
    return FileResponse(BASE/'sample_data'/(name+'.csv'),media_type='text/csv',filename=name+'.csv')
@api.post('/api/analyze')
def analyze(payload:AnalysisRequest):
    try:
        if (payload.csv_text is None)==(payload.records is None):
            raise ValueError('Supply exactly one of csv_text or records.')
        records=parse_csv(payload.csv_text) if payload.csv_text is not None else payload.records
        if len(records)>20_000:raise ValueError('This prototype supports up to20,000 coupon records per analysis.')
        return analyze_records(records,lsl=payload.lsl,usl=payload.usl,baseline_builds=payload.baseline_builds,target=payload.target)
    except (ValueError,OverflowError) as exc:
        raise HTTPException(status_code=422,detail=str(exc)) from exc
