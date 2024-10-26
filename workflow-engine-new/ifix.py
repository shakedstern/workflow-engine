from fastapi import FastAPI, BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from producer import send_messages
from datetime import datetime
from process import process_collection


def validate_computer(country_name: str):
    try:
        query_filter = {"country_name": country_name}
        update_operation = {"$set": {"status": "validate computer"}}
        process_collection.update_one(query_filter, update_operation)
        print(f"Country {country_name} is valid")
    except Exception as e:
        query_filter = {"country_name": country_name}
        update_operation = {"$set": {"status": "Invalid country"}}
        process_collection.update_one(query_filter, update_operation)
        print(f"Error: {str(e)}")


def remove_temp(country_name: str):
    pass
def generate_file(country_name: str):
    pass
def result_agent(country_name: str):
    query_filter = {"country_name": country_name}
    update_operation = {"$set": {"status": "complete"}}
    process_collection.update_one(query_filter, update_operation)
    print(f"Process for {country_name} is complete")


def workflowspace( computer_name: str):
    validate_computer(computer_name)
    remove_temp(computer_name)
    generate_file(computer_name)
    result_agent(computer_name)

def update_policy(country_name: str):
    pass
def install_client(country_name: str):
    pass
def result_client(country_name: str):
    pass
def workflownunstallclient(country_name: str, computer_name: str):
    validate_computer(computer_name)
    update_policy(computer_name)
    install_client(computer_name)
    result_client(computer_name)
    result_agent(computer_name)

