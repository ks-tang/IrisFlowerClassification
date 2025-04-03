from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, #niveau minimum des messages affichés
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", #format des messages
    handlers=[logging.StreamHandler()] # envoie des logs dans la console
)
logger = logging.getLogger("FastAPI Iris Predictor")


# Init de fastapi
app = FastAPI()

# Load du model
try:
    model = joblib.load('model.pkl')
    logger.info("Model loaded successfully")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    raise RuntimeError(status_code=500, detail="Error loading model")


# Pour utiliser les fichiers dans le dossier static
app.mount("/static", StaticFiles(directory="static"), name="static")

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

variety_mapping = {0: 'Setosa', 1: 'Versicolor', 2: 'Virginica'}


# Home endpoint
@app.get("/", response_class=HTMLResponse)
# ajouter response_class=HTMLResponse indique a fastapi que la reponse sera du html et non du json (par defaut)
async def home():
    #return {"message": "Welcome to the Iris Species Predictor API."}

    try:
        # Utilise index.html
        with open("static/index.html", "r") as file:
            logger.info("Home page served")
            return file.read()
    except Exception as e:
        logging.error(f"Error serving home page: {e}")
        return HTMLResponse(status_code=500, content="Error loading home page")

@app.get("/predict", response_class=HTMLResponse) 
# ajouter response_class=HTMLResponse indique a fastapi que la reponse sera du html et non du json (par defaut)
async def predict():

    try:
        with open("static/predict.html", "r") as file:
            logger.info("Predict page served")
            return file.read()
    except Exception as e:
        logging.error(f"Error serving home page: {e}")
        return HTMLResponse(status_code=500, content="Error loading predict page")

# Prediction endpoint
@app.post("/predict")
# async def predict(input: IrisInput):

#     # Probleme :
#     # Nom des colonnes du train : sepal.length, sepal.width, petal.length et petal.width
#     # Nom des colonnes du input : sepal_length, sepal_width, petal_length et petal_width
#     # on convertit le input pour adapter au train
async def predict_variety(sepal_length: float = Form(...),
                          sepal_width: float = Form(...),
                          petal_length: float = Form(...),
                          petal_width: float = Form(...)):
    # column_mapping = {
    #     "sepal_length": "sepal.length",
    #     "sepal_width": "sepal.width",
    #     "petal_length": "petal.length",
    #     "petal_width": "petal.width"
    # }

    # input_dict = {column_mapping[k]: v for k, v in input.dict().items()}
    # input_df = pd.DataFrame([input_dict])

    try:
        input_dict = {"sepal.length": sepal_length, "sepal.width": sepal_width, "petal.length": petal_length, "petal.width": petal_width}
        input_df = pd.DataFrame([input_dict])
        logger.info(f"Input data received: {input_df}")

        prediction = model.predict(input_df)[0]
        variety = variety_mapping.get(prediction, "Unknown")
        logger.info(f"Prediction made: {variety}")

        return {"prediction": variety}
    
    except Exception as e:
        logging.error(f"Error making prediction: {e}")
        return JSONResponse(status_code=500, content={"error": "Failed to make a prediction"})


# uvicorn main:app --reload