from services.health_engine import calculate_machine_learning

result = calculate_machine_learning(
    temperature = 75,
    vibration = 1.8,
    rpm = 1800,
    current = 9,
    power = 4.5
)
print(result)