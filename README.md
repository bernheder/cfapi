# Pandora Calibration-File REST API
This is a REST API for Pandora Calibration-Files.

It is a simple service that allows users to download and query calibration files. 

## Prerequisites
Download the calibration files from the [web](https://data.pandonia-global-network.org/calibrationfiles/).

## Installation
1. Clone the repo
2. Cd into the repo
3. Build the Docker image
```sh
docker build --build-arg USER_ID=1000 --build-arg GROUP_ID=1000 -t cfapi .
```
4. Run the Docker container
```sh
docker run -d -p 4001:4001 -e PORT=4001 -e DATA_FOLDER=/app/data -e DATABASE=dev.db -v /path/to/claibration/files:/app/data cfapi
```


## Usage
The API has three endpoints:
1. GET /
2. GET /calibration-files
3. GET /calibration-files/{id}

### GET /
This endpoint returns details about the API

### GET /calibration-files
This endpoint returns a list of all calibration files.
Can be filtered by setting query parameter "show_field" to the field you want to filter by.  

For example:
http://localhost:4001/calibration-files?show_field=indices_of_warm_pixels

**Fields are lowercased and separated by underscores.**

### GET /calibration-files/{id}
This endpoint returns the full calibration file by id.

For example:
http://localhost:4001/calibration-files/Pandora31s1_CF_v1d20191017.txt

