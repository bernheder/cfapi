from datetime import datetime
from fastapi import FastAPI, Query, Request
import os
from .crud import CalibrationFile, init_db, store_file, get_files, get_file
from .config import DATA_FOLDER


def parse_calibration_file(file_name: str) -> CalibrationFile:
    file_path = os.path.join(DATA_FOLDER, file_name)
    modified_at = datetime.fromtimestamp(os.path.getmtime(file_path))
    with open(file_path, 'r') as file:
        lines = file.readlines()
    data = {}
    for line in lines:
        key, value = line.split('->')
        key = key.strip().lower().replace(' ', '_')
        value = value.strip()
        data[key] = value
    return CalibrationFile(file_name, modified_at, data)


files = os.listdir(DATA_FOLDER)
init_db()
for file in files:
    # TODO: Should check if file in database is older than file in folder,
    #  could be triggered on restart or through polling, using watchdog or even api endpoint
    file = parse_calibration_file(file)
    store_file(file)

# TODO: Create OpenAPI documentation
app = FastAPI()
@app.get("/")
async def root(request: Request):
    base_url = request.base_url
    return {
       "endpoints": [f"{base_url}calibration-files", f"{base_url}calibration-files/{{file_name}}"],
        "examples": {
            "calibration-files": {
                "url": f"{base_url}calibration-files?show_field=indices_of_warm_pixels",
                "query_params": "show_field",
                "description": "Get all calibration files. Optionally filter by field name."
            },
            "calibration-files/{file_name}": {
                "url": f"{base_url}calibration-files/Pandora31s1_CF_v1d20191017.txt",
                "description": "Get a specific calibration file."
            }
        }
    }


@app.get("/calibration-files")
async def get_calibration_files(show_field:  str = Query(None)):
    show_field = show_field if show_field else None
    all_files = get_files(show_field)
    payload = [
        {
            "file_name": file[0],
            "modified_at": file[1],
            show_field: file[2] if show_field else None}
        for file in all_files
    ]
    return payload


@app.get("/calibration-files/{file_name}")
async def get_calibration_file(file_name: str):
    file = get_file(file_name)
    return file[2]
