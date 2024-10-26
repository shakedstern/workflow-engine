from process import process_collection


def validate_computer(computer_name: str):
    try:
        query_filter = {"computer_name": computer_name}
        update_operation = {"$set": {"status": "validate computer"}}
        process_collection.update_one(query_filter, update_operation)
        print(f"Country {computer_name} is valid")
    except Exception as e:
        query_filter = {"computer_name": computer_name}
        update_operation = {"$set": {"status": "Invalid country"}}
        process_collection.update_one(query_filter, update_operation)
        print(f"Error: {str(e)}")


def result_client(computer_name: str):
    query_filter = {"computer_name": computer_name}
    update_operation = {"$set": {"status": "complete"}}
    process_collection.update_one(query_filter, update_operation)
    print(f"Process for {computer_name} is complete")

def remove_temp(computer_name: str):
    pass

def generate_file(computer_name: str):
    pass

def update_policy(computer_name: str):
    pass

def install_client(computer_name: str):
    pass



def start(computer_name: str):
    validate_computer(computer_name)
    update_policy(computer_name)
    install_client(computer_name)
    result_client(computer_name)
    