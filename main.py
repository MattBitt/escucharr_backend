from fastapi import FastAPI
import uvicorn

from routers import (
    itemrouter,
    source_router,
    track_router,
    album_router,
    word_router,
    producer_router,
    tag_router,
)

from data_generator import generate_fake_data

app = FastAPI()
app.include_router(itemrouter)
app.include_router(source_router)
app.include_router(track_router)
app.include_router(album_router)
app.include_router(word_router)
app.include_router(producer_router)
app.include_router(tag_router)
generate_fake_data()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)
