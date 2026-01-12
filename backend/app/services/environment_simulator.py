import random

def simulate_rainfall(current):
    change = random.uniform(-5, 10)
    return max(0, round(current + change, 1))

def simulate_water_level(current):
    change = random.uniform(-3, 6)
    return max(0, round(current + change, 1))