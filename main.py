from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def hello_world():
    return {"msg": "Hello world"}


@app.get("/{my_name}")
async def say_hello(my_name: str) -> dict:
    return {"my_name": my_name, "msg": f"Hello {my_name}!"}
