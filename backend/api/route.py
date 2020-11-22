from fastapi import (
    FastAPI,
    HTTPException,
)
import requests
import json
from typing import List
from pathlib import os
from datetime import datetime
from data.web_scraper_v1 import scrape_wrapper

app = FastAPI()


@app.post("/data/extract")
async def extract_web_data(category: str):
    response = scrape_wrapper(category)
    return response
