import uvicorn
from fastapi import FastAPI

from models import Models, Model
from requests import Requests, Request

app = FastAPI()
models = Models()
requests = Requests(models)


@app.post("/models/create")
def add_model(new_model: Model):
    try:
        models.add_model(new_model)
        return {"status": "success"}
    except Exception as e:
        return {
            "status": "failed uploading model",
            "message": str(e)
        }


# TODO: convert to get
@app.post("/requests/validate")
async def validate_request(request: Request):
    try:
        return await requests.validate_request(request.dict())
    except Exception as e:
        return {
            "status": "failed validating request",
            "message": str(e)
        }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
