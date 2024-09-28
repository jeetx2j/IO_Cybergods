import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import datetime

# Define a Machine class
class Machine:
    def __init__(self, udi, product_id, machine_type):
        self.udi = udi
        self.product_id = product_id
        self.machine_type = machine_type
        self.air_temperature = 0  # Kelvin
        self.process_temperature = 0  # Kelvin
        self.rotational_speed = 0  # rpm
        self.torque = 0  # Nm
        self.tool_wear = 0  # minutes
        self.machine_failure = 0  # binary indicator
        self.twf = 0  # Tool Wear Factor
        self.hdf = 0  # Heat Dissipation Factor
        self.pwf = 0  # Power Wear Factor
        self.osf = 0  # Oil Status Factor
        self.rnf = 0  # Rust and Noise Factor

    def monitor_air_temperature(self, temperature):
        if temperature < 250 or temperature > 350:
            print("Air temperature out of range! Regular cleaning of air filters, ensuring proper ventilation, and monitoring temperature to prevent overheating.")
        self.air_temperature = temperature

    def monitor_process_temperature(self, temperature):
        if temperature < 250 or temperature > 500:
            print("Process temperature out of range! Treatment: Implementing temperature control systems, using thermal insulation, and monitoring temperature to prevent overheating.")
        self.process_temperature = temperature

    def monitor_rotational_speed(self, speed):
        if speed < 0 or speed > 10000:
            print("Rotational speed out of range! Treatment: Regular balancing and alignment of rotating equipment, monitoring vibration, and performing predictive maintenance.")
        self.rotational_speed = speed

    def monitor_torque(self, torque):
        if torque < 0 or torque > 1000:
            print("Torque out of range! Treatment: Regular inspection and maintenance of gearboxes, monitoring torque levels, and performing predictive maintenance.")
        self.torque = torque

    def monitor_tool_wear(self, wear):
        if wear < 0 or wear > 1000:
            print("Tool wear out of range! Treatment: Implementing tool wear monitoring systems, performing regular tool maintenance, and optimizing tool replacement schedules.")
        self.tool_wear = wear

    def check_machine_failure(self):
        if self.machine_failure == 1:
            print("Machine failure detected! Treatment: Implementing predictive maintenance, performing regular inspections, and having a maintenance plan in place.")
        else:
            print("Machine is operating normally.")

    def calculate_twf(self):
        # implement calculation for Tool Wear Factor
        self.twf = 0.5  # example value

    def calculate_hdf(self):
        # implement calculation for Heat Dissipation Factor
        self.hdf = 0.7  # example value

    def calculate_pwf(self):
        # implement calculation for Power Wear Factor
        self.pwf = 0.3  # example value

    def calculate_osf(self):
        # implement calculation for Oil Status Factor
        self.osf = 0.9  # example value

    def calculate_rnf(self):
        # implement calculation for Rust and Noise Factor
        self.rnf = 0.1  # example value

    def print_machine_status(self):
        print("Machine Status:")
        print(f"UDI: {self.udi}")
        print(f"Product ID: {self.product_id}")
        print(f"Machine Type: {self.machine_type}")
        print(f"Air Temperature: {self.air_temperature} K")
        print(f"Process Temperature: {self.process_temperature} K")
        print(f"Rotational Speed: {self.rotational_speed} rpm")
        print(f"Torque: {self.torque} Nm")
        print(f"Tool Wear: {self.tool_wear} minutes")
        print(f"Machine Failure: {self.machine_failure}")
        print(f"TWF: {self.twf}")
        print(f"HDF: {self.hdf}")
        print(f"PWF: {self.pwf}")
        print(f"OSF: {self.osf}")
        print(f"RNF: {self.rnf}")

# Load dataset from CSV file
equipment_data = pd.read_csv('datasets/ai4i2020.csv')

# Define features and target variable
X = equipment_data.drop(['Machine failure'], axis=1)
y = equipment_data['Machine failure']

# Encode categorical columns using LabelEncoder
le = LabelEncoder()
X['UDI'] = le.fit_transform(X['UDI'])
X['Product ID'] = le.fit_transform(X['Product ID'])
X['Type'] = le.fit_transform(X['Type'])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train random forest classifier
rfc = RandomForestClassifier(n_estimators=100, random_state=42)
rfc.fit(X_train, y_train)

# Make predictions on test data
y_pred = rfc.predict(X_test)

# Evaluate model performance
accuracy = accuracy_score(y_test, y_pred)
print(f'Model accuracy: {accuracy:.3f}')
print(classification_report(y_test, y_pred))

# Define maintenance scheduling function
def schedule_maintenance(equipment_data, rfc):
    # Encode categorical columns using LabelEncoder
    le = LabelEncoder()
    equipment_data['UDI'] = le.fit_transform(equipment_data['UDI'])
    equipment_data['Product ID'] = le.fit_transform(equipment_data['Product ID'])
    equipment_data['Type'] = le.fit_transform(equipment_data['Type'])
    
    # Predict probability of failure for each equipment
    probabilities = rfc.predict_proba(equipment_data.drop(['Machine failure'], axis=1))[:, 1]
    
    # Create a schedule dataframe
    schedule = pd.DataFrame({'UDI': equipment_data['UDI'],
                             'Product ID': equipment_data['Product ID'],
                             'Type': equipment_data['Type'],
                             'probability_of_failure': probabilities,
                             'maintenance_priority': np.where(probabilities > 0.5, 'High', 'Low'),
                             'maintenance_window': np.where(equipment_data['Type'] == 'Day', 'Morning', 'Afternoon')})
    
    # Sort schedule by priority and maintenance window
    schedule = schedule.sort_values(['maintenance_priority', 'maintenance_window'])
    
    return schedule

# Encode categorical columns using LabelEncoder
le = LabelEncoder()
equipment_data['UDI'] = le.fit_transform(equipment_data['UDI'])
equipment_data['Product ID'] = le.fit_transform(equipment_data['Product ID'])
equipment_data['Type'] = le.fit_transform(equipment_data['Type'])

# Schedule maintenance tasks
schedule = schedule_maintenance(equipment_data, rfc)

# Print maintenance schedule
print(schedule.head(10))

# Define real-time alert function
def send_alert(UDI, probability_of_failure):
    if probability_of_failure > 0.7:
        print(f'Alert: Equipment {UDI} has a high probability of failure ({probability_of_failure:.2f}). Schedule maintenance immediately!')
    elif probability_of_failure > 0.5:
        print(f'Warning: Equipment {UDI} has a moderate probability of failure ({probability_of_failure:.2f}). Schedule maintenance soon.')

# Create a machine object
machine1 = Machine("UDI-123", "Product-ABC", "Type-X")
machine1.monitor_air_temperature(500)
machine1.monitor_process_temperature(400)
machine1.monitor_rotational_speed(5000)
machine1.monitor_torque(500)
machine1.monitor_tool_wear(300)
machine1.check_machine_failure()
machine1.calculate_twf()
machine1.calculate_hdf()
machine1.calculate_pwf()
machine1.calculate_osf()
machine1.calculate_rnf()
machine1.print_machine_status()

# Send real-time alert
send_alert(machine1.udi, 0.8)