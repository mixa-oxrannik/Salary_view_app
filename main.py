import uvicorn
from fastapi import FastAPI

import routers

app = FastAPI()
app.include_router(routers.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)