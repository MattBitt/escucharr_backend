from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from db import Base, engine
from my_logging import setup_logging

from routers import (
    source_router,
    track_router,
    album_router,
    word_router,
    producer_router,
    tag_router,
    beat_router,
    artist_router,
)

logger = setup_logging()


app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(source_router)
app.include_router(track_router)
app.include_router(album_router)
app.include_router(word_router)
app.include_router(producer_router)
app.include_router(tag_router)
app.include_router(beat_router)
app.include_router(artist_router)


# Should include a health check for the postgres db
# had a situation where nothing was working, because the db
# needed to be restarted


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run("main:app", port=9000, reload=True)
