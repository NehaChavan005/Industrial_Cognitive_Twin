def calculate_machine_health(
    temperature,
    vibration,
    rpm,
    current,
    power
):

    score = 100
    #Temperature analysis
    if temperature > 80:
        score -= 30
    elif temperature > 70:
        score -= 15

    #Vibration analysis
    if vibration > 2.5:
        score -= 30
    elif vibration > 1.5:
        score -= 15

    #RPM analysis
    if rpm < 1600:
        score -= 15
    elif rpm > 2000:
        score -= 15
    
    #Current analysis
    if current > 12:
        score -= 15
    elif current > 10:
        score -= 5

    #Power analysis
    if power > 6:
        score -= 10

    #MAke sure score doesn't go below zero
    score = max(score, 0)

    #Determine machine status
    if score >= 80:
        status = "NORMAL"
    elif score >= 50:
        status = "WARNING"
    else:
        status = "CRITICAL"

    return{
        "health_score": score,
        "status": status
    }