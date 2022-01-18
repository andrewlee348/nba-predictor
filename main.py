from enum import Enum
from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI(
    title="home_api"
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test/{model_name}", tags=["test"])
async def test(model_name: ModelName, page: int = 0, limit: int = 10):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!", "page": page, "limit": limit}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}