import random 
from datetime import datetime
import time
from faker import Faker

#utilities func
fake = Faker()

def random_user():
    return fake.name()


def current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# attack func
def generateNormal():
    data = {
        "ip": fake.ipv4(),
        "port": random.choice([22, 80, 443, 3306]),
        "country": fake.country_code(),
        "timestamp": current_timestamp(),
        "username": random_user(),
        "status": "success",
        "protocol": "tcp",
        "count": random.randint(1, 5),
        "duration": round(random.uniform(1, 5), 2),
        "src_bytes": random.randint(300, 1500),
        "dst_bytes": random.randint(2000, 6000),
        "label": "normal"
    }
    return data

def generateBruteForce():
    data = {
        "ip": fake.ipv4(),
        "port": random.choice([22, 80, 443, 3306]),
        "country": fake.country_code(),
        "timestamp": current_timestamp(),
        "username": random_user(),
        "status": "success",
        "protocol": "tcp",
        "count": random.randint(30,200),
        "duration": round(random.uniform(0.05,0.3), 2),
        "src_bytes": random.randint(40, 150),
        "dst_bytes": random.randint(0,200),
        "label": "bruteforce"
    }
    return data

def generateDos():
    data = {
        "ip": fake.ipv4(),
        "port": random.choice([22, 80, 443, 3306]),
        "country": fake.country_code(),
        "timestamp": current_timestamp(),
        "username": random_user(),
        "status": "none",
        "protocol": "tcp",
        "count": random.randint(200, 2000),
        "duration": round(random.uniform(0.01,0.1), 3),
        "src_bytes": random.randint(30, 200),
        "dst_bytes": random.randint(0, 200),
        "label": "dos"
    }
    return data

def generateUdp():
    data = {
        "ip": fake.ipv4(),
        "port": random.choice([22, 80, 443, 3306]),
        "country": fake.country_code(),
        "timestamp": current_timestamp(),
        "username": random_user(),
        "status": "success",
        "protocol": "tcp",
        "count": random.randint(100, 500),
        "duration": round(random.uniform(0.05, 0.3), 3),
        "src_bytes": random.randint(20,200),
        "dst_bytes": 0,
        "label": "udpFlood"
        
    }
    return data

def generateAnomaly():
    data = {
        "ip": fake.ipv4(),
        "port": random.choice([22, 80, 443, 3306]),
        "country": fake.country_code(),
        "timestamp": current_timestamp(),
        "username": random_user(),
        "status": random.choice(["success", "failed", "none"]),
        "protocol": random.choice(["tcp", "udp"]),
        "count": random.randint(10, 20),
        "duration": round(random.uniform(6, 20), 2),
        "src_bytes": random.randint(2000, 20000),
        "dst_bytes": random.randint(100, 6000),
        "label": "anomaly"
    }
    return data