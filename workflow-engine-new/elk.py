from elasticsearch import Elasticsearch


# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Function to send results to Elasticsearch
def send_result_to_elasticsearch(es, document):
    for item in document:
        res = es.index(index="ip_segment", document=item)
        print(res['result']) 

# Prepare scan results for Elasticsearch

# Your function to scan the network and process results
def process_and_send_results(result_document):
    print("sent to elastic")
    send_result_to_elasticsearch(es, result_document)

# Example usage after scanning IPs

