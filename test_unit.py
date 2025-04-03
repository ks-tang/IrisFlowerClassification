import pytest
from main import model, variety_mapping
import pandas as pd 

def test_model_prediction():
    input_df = pd.DataFrame([[5.1, 3.5, 1.4, 0.2]],
                            columns=["sepal.length", "sepal.width", "petal.length", "petal.width"])
    
    print(input_df)
    prediction = model.predict(input_df)[0]
    variety = variety_mapping.get(prediction, "Unknown")

    assert variety == "Setosa", 'The prediction did not return the expected result'

