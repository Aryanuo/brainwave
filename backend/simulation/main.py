# Imports
import random 
import  requests
import time

from attack import generateNormal
from attack import generateAnomaly
from attack import generateBruteForce
from attack import generateDos
from attack import generateUdp


API_URL = "http://localhost:5000/logs"   

def run_main():
    i=0
    while i<4:
        choice = random.randint(1,100)

        if (1<=choice<=70) :
            record = generateNormal()

        elif (70<choice<81):
            record = generateBruteForce()

        elif (81<=choice<=88):
            record = generateDos()

        elif (89<=choice<=95):
            record = generateUdp()

        elif (96<choice<100):
            record = generateAnomaly()

        try:
            response = requests.post(API_URL, json=record)
            print("Sent:", record)
            print("Response:", response.json())
        except Exception as e:
            print("API not reachable:", e)

        time.sleep(5)
        i +=1 
        print("\n--- TESTING GET ENDPOINT ---")
        try:
            get_res = requests.get(API_URL)
            print(f"Status: {get_res.status_code}")
            if get_res.status_code == 200:
                data = get_res.json()
                print(f"Records found:",data)
        except Exception as e:
            print(f"Error connecting to GET: {e}")

if __name__ == "__main__":
    run_main()