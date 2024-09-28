import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import datetime

# Load equipment usage and performance data
equipment_data = pd.read_csv('/home/cybergod/Documents/hacathonsmartodisha/datasets/ai4i2020.csv')

# Define columns of interest
columns = ['UDI', 'Product ID', 'Type', 'Air temperature [K]', 'Process temperature [K]', 
           'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]', 'Machine failure', 
           'TWF', 'HDF', 'PWF', 'OSF', 'RNF']

# Select columns of interest from the equipment data
equipment_data = equipment_data[columns]

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