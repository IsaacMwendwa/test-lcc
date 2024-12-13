#!/bin/bash

# Function to get the current CPU utilization
get_cpu_utilization() {
    local cpu_util=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
    echo $cpu_util
}

# Function to get the notebook instance status
get_notebook_status() {
    local status=$(aws sagemaker describe-notebook-instance --notebook-instance-name test-notebook-lcc --query "NotebookInstanceStatus" --output text)
    echo "$status"
}

# Main loop to check CPU utilization and stop the instance if needed
while true; do
    cpu_util=$(get_cpu_utilization)
    if (( $(echo "$cpu_util > 1" | bc -l) )); then
        notebook_status=$(get_notebook_status)

        if [ "$notebook_status" == "InService" ]; then
            aws sagemaker stop-notebook-instance --notebook-instance-name test-notebook-lcc
            echo "Notebook instance stopped due to high CPU utilization ($cpu_util%)"
            break
        else
            echo "Notebook instance is not in InService status ($notebook_status). Skipping stop."
        fi
    fi
    sleep 60  # Check CPU utilization every 60 seconds
done
