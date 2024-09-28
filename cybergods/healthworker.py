def measure_systolic_blood_pressure(systolic_pressure):
    if systolic_pressure <= 100:
        return "low systolic pressure"
    elif systolic_pressure >= 130:
        return "high systolic pressure"
    else:
        return "healthy"
def measure_diastolic_blood_pressure(diastolic_pressure):
    if diastolic_pressure <= 70:
        return "low diastolic pressure"
    elif diastolic_pressure >= 90:
        return "high diastolic pressure"
    else:
        return "healthy"
def measure_oxygen_level(oxygen_level):
    if oxygen_level <= 70:
        return "low oxygen level"
    else:
        return "healthy"
def measure_body_temprature(body_temprature):
    if body_temprature > 98.4:
        return "high temprature"
    else:
        return "healthy"
def measure_heart_beat(heart_beat):
    if heart_beat <= 50:
        return "emergency"
    elif heart_beat >= 90:
        return "emergency"
    else:
        return "healthy"
def measure_breathing_rate(breathing_rate):
    if breathing_rate >= 30:
        return "need rest"
    elif breathing_rate <= 10:
        return "critical condition"
    else:
        return "healthy"
# Test the function
systolic_pressure = float(input("Enter your systolic blood pressure: "))
diastolic_pressure = float(input("Enter your diastolic blood pressure: "))
oxygen_level = float(input("Enter Oxygen Level:"))
body_temprature = float(input("Enter Body Temprature:"))
heart_beat = float(input("Enter Heart Beat:"))
breathing_rate = float(input("Enter Breathing Ratel:"))
result = measure_systolic_blood_pressure(systolic_pressure)
result1 = measure_diastolic_blood_pressure(diastolic_pressure)
result2 = measure_oxygen_level(oxygen_level)
result3 = measure_body_temprature(body_temprature)
result4 = measure_heart_beat(heart_beat)
result5 = measure_breathing_rate(breathing_rate)

print(f"Your systolic blood pressure is {result}")
print(f"Your diastolic blood pressure is {result1}")
print(f"Your Oxygen level is {result2}")
print(f"Your Body temprature is {result3}")
print(f"Your Heart Beat is {result4}")
print(f"Your Breathing Rate is {result5}")