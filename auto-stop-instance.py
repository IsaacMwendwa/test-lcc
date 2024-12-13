import time
import psutil
import boto3

# Function to get the current CPU utilization
def get_cpu_utilization():
    cpu_util = psutil.cpu_percent(interval=1)
    return cpu_util

# Function to get the notebook instance status
def get_notebook_status(notebook_instance_name):
    sagemaker_client = boto3.client('sagemaker')
    response = sagemaker_client.describe_notebook_instance(
        NotebookInstanceName=notebook_instance_name
    )
    status = response['NotebookInstanceStatus']
    return status

# Main loop to check CPU utilization and stop the instance if needed
notebook_instance_name = 'test-notebook-lcc'

while True:
    cpu_util = get_cpu_utilization()
    if cpu_util > 1:
        notebook_status = get_notebook_status(notebook_instance_name)

        if notebook_status == 'InService':
            sagemaker_client = boto3.client('sagemaker')
            sagemaker_client.stop_notebook_instance(
                NotebookInstanceName=notebook_instance_name
            )
            print(f"Notebook instance stopped due to high CPU utilization ({cpu_util}%)")
            break
        else:
            print(f"Notebook instance is not in InService status ({notebook_status}). Skipping stop.")

    time.sleep(60)  # Check CPU utilization every 60 seconds
