from fastapi import FastAPI
from process import create_process, get_all_processes, get_process

app = FastAPI()

@app.post("/process/")
async def create_process_route(computer_name:str ,type: str):
    return await create_process(computer_name=computer_name,type=type)


@app.get("/process/{id}")
async def get_process_route(id: str):
    return await get_process(id)


@app.get("/processes")
async def get_all_processes_route():
    return await get_all_processes()
