import pytest
from fastapi.testclient import TestClient
from route import app  # Replace with your actual FastAPI app import

# Create a TestClient instance
client = TestClient(app)

# Test case for creating a new process
def test_create_process():
    url = "/process"  # You don't need the full URL with TestClient
    new_process = {"computer_name": "824shakeds", "type": "check segment"}
    
    response = client.post(url, json=new_process)  # Use `json` instead of `params`
    
    # Check if the response status code is 200 OK
    assert response.status_code == 200

# Test case for getting a process by ID
def test_get_process_route():
    process_id = "6713d0d698ad31f506317404"
    url = f"/process/{process_id}"
    
    response = client.get(url)
    
    # Check if the response status code is 200 OK
    assert response.status_code == 200

# Test case for getting all processes
def test_get_all_processes_route():
    url = "/processes"
    
    response = client.get(url)
    
    # Check if the response status code is 200 OK
    assert response.status_code == 200
