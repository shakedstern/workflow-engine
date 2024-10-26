import pprint
import socket
from models import Result
from process import process_collection
from pythonping import ping
from bson import ObjectId
import elk

def find_ip_from_dns(server_name: str,id:str):
    try:
        ip_address = socket.gethostbyname(server_name)

        # Return a custom object to mimic TCPHost behavior
        return ip_address
    except socket.gaierror:
        query_filter = {"_id": ObjectId(id)}
        update_operation = {"$set": {"status": "get ip-failed"}}
        process_collection.update_one(query_filter, update_operation)
        raise Exception(f"Could not resolve DNS: {server_name}")
        
    
# Check if the DNS exists; if it does, it will return the IP of this server
def check_dns(ip_address: str):
        
        response = ping(ip_address, count=1, timeout=0.2)

        # Return a custom object to mimic TCPHost behavior
        return {
            'ip_address': ip_address,
            'is_alive': response.success()  # Check if the ping was successful
        }
    #except socket.gaierror:
        #query_filter = {"computer_name": server_name}
       # update_operation = {"$set": {"status": "check ping-failed"}}
        #process_collection.update_one(query_filter, update_operation)
        #raise Exception(f"Could not resolve ping: {ip_address}")

def get_ips_in_segment(segment: str, server_name: str,id:str):
    query_filter = {"_id": ObjectId(id)}
    update_operation = {"$set": {"status": "get ips"}}
    process_collection.update_one(query_filter, update_operation)
    ips_list = []
    address = segment.split('.')
    
    if len(address) != 4:
        query_filter = {"_id": ObjectId(id)}
        update_operation = {"$set": {"status": "get ips-failed"}}
        process_collection.update_one(query_filter, update_operation)
        raise Exception("IP address not valid")
        
    for i in range(10):  # Range is 256 to include .255
        address[3] = str(i)
        ips_list.append(".".join(address))
    return ips_list

def check_for_available_ips_in_segment(ip_addresses: list[str], server_name: str,id:str):
    try:
        query_filter = {"_id": ObjectId(id)}
        update_operation = {"$set": {"status": "check all computers on segment"}}
        process_collection.update_one(query_filter, update_operation)
        unavailable = []
        available = []
        
        for address in ip_addresses:
            current_tcp_host = check_dns(address)
            if current_tcp_host['is_alive']:
                dns_name = socket.gethostbyaddr(current_tcp_host['ip_address'])[0]
                available.append({"address": current_tcp_host['ip_address'], "dns": dns_name})
            else:
                unavailable.append({"address": current_tcp_host['ip_address'], "dns": ""})
        
        return {"unavailable": unavailable, "available": available}
    except Exception as e:
        query_filter = {"_id": ObjectId(id)}
        update_operation = {"$set": {"status": "check all computers on segment-fail"}}
        process_collection.update_one(query_filter, update_operation)
        print(f"An error occurred while check segment: {e}")


def convert_json(result:dict,id:str):
    query_filter = {"_id": ObjectId(id)}
    update_operation = {"$set": {"status": "complete -sends to kibana data"}}
    process_collection.update_one(query_filter, update_operation)
    new =[]
    for item in result["unavailable"]:
        item["available"]=False
        new.append(item)
    for item in result["available"]:
        item["available"]=True
        new.append(item)
    return new
        

# Input: DNS
# Output: Two lists, one for unavailable servers in the same segment, the other for available DNS names.
def start(ip_address:str ,id:str):
    query_filter = {"_id": ObjectId(id)}
    update_operation = {"$set": {"status": "validate computer","result":None}}
    
    process_collection.update_one(query_filter, update_operation)
  
    ip=find_ip_from_dns(ip_address,id=id)
    host = check_dns(ip)
    ip_list = get_ips_in_segment(segment=host['ip_address'], server_name=ip_address,id=id)
    result = check_for_available_ips_in_segment(ip_addresses=ip_list, server_name=ip_address,id=id)
    update_result = {"$set": {"result": Result(is_failed=False,result_dict=result).model_dump_json()}}
    process_collection.update_one(query_filter, update_result)
    jsonelk=convert_json(result=result,id=id)
    print("Data to be sent to Elasticsearch:", jsonelk)  # Debugging line
    elk.process_and_send_results(jsonelk)
    pprint.pprint(result)


    return result

if __name__ == "__main__":
    pprint.pprint(start("www.google.com"))


