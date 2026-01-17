import requests
import time
import os


WORKFLOW_ID = "696a15de8e6b21cb8aea4002"

API_KEY = os.getenv("ONDEMAND_API_KEY", "i9LLNRIMTf0ESxVsMr88d6NwDBTDHXBr")

EXECUTE_URL = f"https://api.on-demand.io/automation/api/workflow/{WORKFLOW_ID}/execute"
STATUS_URL = "https://api.on-demand.io/automation/api/execution/{}"

HEADERS = {
    "apikey": API_KEY,
    "Content-Type": "application/json"
}


def start_workflow(failed_logins: int, request_rate: int, data_size: int) -> dict:
    """
    Starts the on-demand workflow and returns executionID
    """
    payload = {
        "input": {
            "failedlogins": failed_logins,
            "requestrate": request_rate,
            "data_size": data_size
        }
    }

    response = requests.post(
        EXECUTE_URL,
        json=payload,
        headers=HEADERS,
        timeout=15
    )
    response.raise_for_status()
    return response.json()



def poll_execution_once(execution_id: str) -> dict:
    """
    Fetches current execution status/output (non-blocking)
    """
    response = requests.get(
        STATUS_URL.format(execution_id),
        headers={"apikey": API_KEY},
        timeout=15
    )
    response.raise_for_status()
    return response.json()




def poll_execution_blocking(
    execution_id: str,
    retries: int = 20,
    delay: int = 0.5
) -> dict:
    """
    Blocks until workflow completes or times out
    """
    for _ in range(retries):
        result = poll_execution_once(execution_id)

        status = result.get("status")

        if status == "COMPLETED":
            return result.get("output", result)

        if status == "FAILED":
            return {
                "error": "Workflow execution failed",
                "details": result
            }

        time.sleep(delay)

    return {
        "error": "Execution still running",
        "executionID": execution_id
    }



def get_threat_report(
    failed_logins: int,
    request_rate: int,
    data_size: int,
    blocking: bool = False
) -> dict:
    """
    Starts workflow and returns:
    - executionID (non-blocking)
    - final output (blocking=True)
    """
    start = start_workflow(failed_logins, request_rate, data_size)

    if "executionID" not in start:
        return start

    execution_id = start["executionID"]

    if blocking:
        return poll_execution_blocking(execution_id)

    return {
        "executionID": execution_id,
        "status": "STARTED"
    }
