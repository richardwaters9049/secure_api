# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from app.authentication import verify_token  # Import auth module
from app.security_utils import rate_limiter  # Import security features
import logging

# Initialise FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)


class Item(BaseModel):
    name: str
    description: str
    price: float


# Secure API Endpoint with Authentication & Rate Limiting
@app.post("/items/", dependencies=[Depends(verify_token), Depends(rate_limiter)])
def create_item(item: Item):
    logging.info(f"New item created: {item.name}")
    return {"message": "Item successfully created", "item": item}


@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
