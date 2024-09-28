import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Step 1: Data Collection and Integration
data = pd.read_csv('/home/cybergod/Documents/hacathonsmartodisha/disaster_data.csv')

# Step 2: Data Preprocessing and Feature Engineering
data.dropna(inplace=True)  # handle missing values
data['elevation'] = pd.to_numeric(data['elevation'])  # convert elevation to numeric

# One-hot encode land use
land_use_dummies = pd.get_dummies(data['land_use'])
data = pd.concat([data, land_use_dummies], axis=1)  # concatenate with original DataFrame
data.drop('land_use', axis=1, inplace=True)  # drop original land_use column

# One-hot encode weather
weather_dummies = pd.get_dummies(data['weather'])
data = pd.concat([data, weather_dummies], axis=1)  # concatenate with original DataFrame
data.drop('weather', axis=1, inplace=True)  # drop original weather column

# One-hot encode disaster type
disaster_type_dummies = pd.get_dummies(data['disaster_type'])
data = pd.concat([data, disaster_type_dummies], axis=1)  # concatenate with original DataFrame
data.drop('disaster_type', axis=1, inplace=True)  # drop original disaster_type column

# Step 3: Machine Learning Model Development
X = data.drop(['damage'], axis=1)  # features
y = data['damage']  # target variable
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 4: Digital Twin Development
def digital_twin(disaster_type, elevation, land_use, weather):
    # simulate disaster scenario using machine learning model
    input_data = pd.DataFrame({'elevation': [elevation]})
    for lu in land_use_dummies.columns:
        if lu in land_use:
            input_data[lu] = [1]
        else:
            input_data[lu] = [0]
    for w in weather_dummies.columns:
        if w in weather:
            input_data[w] = [1]
        else:
            input_data[w] = [0]
    for dt in disaster_type_dummies.columns:
        if dt in disaster_type:
            input_data[dt] = [1]
        else:
            input_data[dt] = [0]
    prediction = model.predict(input_data)
    return prediction

# Step 5: Disaster Response Strategy Optimization
def optimize_response(damage_prediction):
    # optimize response strategy based on damage prediction
    if damage_prediction <= 1000:
        return 'Evacuation'
    elif damage_prediction <= 5000:
        return 'Search and Rescue'
    elif damage_prediction <= 10000:
        return 'Medical Aid'
    elif damage_prediction <= 20000:
        return 'Food and Water Distribution'
    else:
        return 'Full-Scale Response'

# Example usage:
disaster_type = 'Earthquake'
elevation = 30  # meters
land_use = 'Industrial'
weather = 'Cloudy'
damage_prediction = digital_twin(disaster_type, elevation, land_use, weather)
response_strategy = optimize_response(damage_prediction)
print(f'Response strategy: {response_strategy}')