from datetime import date

def calculate_age(birthdate: date) -> int:
    """Calculate age in years from birthdate"""
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def calculate_bmi(weight: float, height: float) -> float:
    """Calculate BMI from weight (kg) and height (m)"""
    if height <= 0:
        return 0.0
    return weight / (height ** 2)

def calculate_health_metrics(pet_data: dict) -> dict:
    """Calculate various health metrics for a pet"""
    weight = float(pet_data.get('weight', 0))
    height = float(pet_data.get('height', 0))
    age = pet_data.get('age', 0)
    species = pet_data.get('species', '').lower()
    
    bmi = calculate_bmi(weight, height)
    
    # Basic health status based on BMI and species
    if species == 'dog':
        if bmi < 15:
            status = 'Underweight'
        elif 15 <= bmi <= 25:
            status = 'Healthy'
        elif 25 < bmi <= 30:
            status = 'Overweight'
        else:
            status = 'Obese'
    elif species == 'cat':
        if bmi < 18:
            status = 'Underweight'
        elif 18 <= bmi <= 27:
            status = 'Healthy'
        elif 27 < bmi <= 32:
            status = 'Overweight'
        else:
            status = 'Obese'
    else:
        status = 'Unknown'
    
    return {
        'bmi': round(bmi, 2),
        'status': status,
        'weight': weight,
        'height': height,
        'age': age
    }
