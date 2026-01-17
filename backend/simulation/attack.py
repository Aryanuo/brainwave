import random
from datetime import datetime
from faker import Faker

fake = Faker()

def random_user():
    return fake.name()

def current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def generateNormal():
    return {
        "Destination Port": random.choice([80, 443, 53]),
        "Flow Duration": random.randint(10000, 100000), 
        "Total Fwd Packets": random.randint(2, 20),
        "Total Backward Packets": random.randint(2, 20),
        "Total Length of Fwd Packets": random.randint(100, 1000),
        "Total Length of Bwd Packets": random.randint(100, 1000),
        "Protocol": 6,
        "timestamp": current_timestamp(),
        "username": random_user()
    }

def generateBruteForce():
    return {
        "Destination Port": 22,
        "Flow Duration": random.randint(1, 10), 
        "Total Fwd Packets": random.randint(10000, 50000),
        "Total Backward Packets": random.randint(5000, 20000),
        "Total Length of Fwd Packets": random.randint(500, 2000),
        "Total Length of Bwd Packets": random.randint(500, 2000),
        "Protocol": 6,
        "timestamp": current_timestamp(),
        "username": "admin"
    }

def generateDos():
    return {
        "Destination Port": 80,
        "Flow Duration": 1, 
        "Total Fwd Packets": random.randint(100000, 500000),
        "Total Backward Packets": 0,
        "Total Length of Fwd Packets": random.randint(5000, 20000),
        "Total Length of Bwd Packets": 0,
        "Protocol": 6,
        "timestamp": current_timestamp(),
        "username": "none"
    }

def generateUdp():
    return {
        "Destination Port": random.randint(1024, 65535),
        "Flow Duration": 1,
        "Total Fwd Packets": random.randint(50000, 150000), 
        "Total Backward Packets": 0,
        "Total Length of Fwd Packets": random.randint(1000, 5000),
        "Total Length of Bwd Packets": 0,
        "Protocol": 17,
        "timestamp": current_timestamp(),
        "username": "none"
    }

def generateAnomaly():
    return {
        "Destination Port": 9999,
        "Flow Duration": 10000000, 
        "Total Fwd Packets": 1,
        "Total Backward Packets": 1,
        "Total Length of Fwd Packets": 50000, 
        "Total Length of Bwd Packets": 50000,
        "Protocol": 0,
        "timestamp": current_timestamp(),
        "username": "unknown"
    }
