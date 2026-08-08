def detect_anomaly(temperature, vibration, rpm, current, power):

    anomalies = []

    if temperature > 85:
        anomalies.append("High Temperature")

    if vibration > 2.5:
        anomalies.append("High Vibration")

    if rpm < 1500:
        anomalies.append("Low RPM")

    if current > 12:
        anomalies.append("High Current")

    if power > 6:
        anomalies.append("High Power Consumption")

    if len(anomalies) == 0:
        return {
            "anomaly": False,
            "issues": []
        }

    return {
        "anomaly": True,
        "issues": anomalies
    }