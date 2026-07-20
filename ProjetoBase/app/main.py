from fastapi import FastAPI

app = FastAPI(
    title="Minha API",
    description="API de exemplo com FastAPI",
    version="1.0.0"
)



@app.get("/")
def root():
    return {"message": "Hello World!"}

@app.get("/item_id1/")
def item_id(id: int):
    return {"message": f"O id informado é {id}"}

@app.get("/item_id1/{item_id2}")
def item_id(item_id2: int):
    return {"message"   : f"O id informado é {item_id2}"}
