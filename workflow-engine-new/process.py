import json
from fastapi import HTTPException
from models import Process
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient

from producer import send_messages


MONGO_DETAILS = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.process
process_collection = database.get_collection("process_collection")


def serialize_mongo_id(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


async def create_process(computer_name:str ,type: str):
    process = Process(status="create",type=type,computer_name=computer_name)
    document = jsonable_encoder(process)
    result = await process_collection.insert_one(document)
    json_string =  json.dumps(document, default=serialize_mongo_id)
    try:
        send_messages("process",json_string)

        return json.dumps(
            document, default=serialize_mongo_id
        ), {"id": str(result.inserted_id), "status": "create", "computer_name":str(document["computer_name"])}
    except Exception as e:
         print(f"An error occurred while fetching processes: {e}")
        

async def get_process(id: str):
    try:
        process = await process_collection.find_one({"_id": ObjectId(id)})
        
        if process:
            process["_id"] = id
            return process
        else:
            #raise Exception ("process not found")
            raise HTTPException(status_code=404, detail="Process not found")

            return {"message": "Process not found"}
    except HTTPException as http_exc:
        # Raise the HTTPException (handled automatically by FastAPI)
        print(f"An error occurred while fetching process: {http_exc}")
        raise http_exc
    except Exception as e:
        print(f"An error occurred while fetching process: {e}")

async def get_all_processes():
    try:
        processes = await process_collection.find().to_list(length=100)
        return [
            {"status": process["status"], "computer_name":str(process["computer_name"])}
            for process in processes
        ]
    except Exception as e:
        print(f"An error occurred while fetching processes: {e}")
        return []  # Return an empty list or handle as needed
