
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
import pandas as pd
import joblib
import os
from datetime import datetime

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
MODEL_PATH = os.path.join(BASE_DIR,"../" "datascience",'notebook_outputs', "models", "model.joblib")
model = None

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.post("/predict-form", response_class=HTMLResponse)
def predict_form(request: Request,
                 sqft_living: float = Form(...),
                 bedrooms: float = Form(...),
                 bathrooms: float = Form(...),
                 floors: float = Form(...),
                 condition: int = Form(...),
                 view: int = Form(...),
                 yr_built: int = Form(...),
                 city: str = Form(...)):

    year_now = datetime.now().year
    house_age = year_now - yr_built
    print(view)

    df = pd.DataFrame([{
        "sqft_living": sqft_living,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "floors": floors,
        "condition": condition,
        "view": view,
        "yr_built": house_age,
        "city": city
    }])
    4
    if model:
        pred = model.predict(df)[0]
        print(pred)
    else:
        pred = 0

    return templates.TemplateResponse("result.html", {"request": request, "prediction": round(float(pred),2)})
