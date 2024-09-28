import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Step 1: Data Collection and Integration
data = pd.read_csv('/home/cybergod/Documents/hacathonsmartodisha/health_data.csv')

# Check if the 'age' column exists in the DataFrame
if 'age' not in data.columns:
    print("The 'age' column does not exist in the DataFrame.")
    exit()

# Step 2: Data Preprocessing and Feature Engineering
data.dropna(inplace=True)  # handle missing values
data['age'] = pd.to_numeric(data['age'])  # convert age to numeric
data['bmi'] = pd.to_numeric(data['bmi'])  # convert bmi to numeric

# One-hot encode categorical variables
categorical_vars = ['sex', 'smoker', 'region']
for var in categorical_vars:
    if var not in data.columns:
        print(f"The '{var}' column does not exist in the DataFrame.")
        exit()
    dummies = pd.get_dummies(data[var], prefix=var)
    data = pd.concat([data, dummies], axis=1)
    data.drop(var, axis=1, inplace=True)

# Step 3: Machine Learning Model Development
X = data.drop(['disease', 'age_of_death'], axis=1)  # features
y_disease = data['disease']  # target variable for disease prediction
y_age_of_death = data['age_of_death']  # target variable for age of death prediction

X_train, X_test, y_train_disease, y_test_disease, y_train_age_of_death, y_test_age_of_death = train_test_split(X, y_disease, y_age_of_death, test_size=0.2, random_state=42)

# Train disease prediction model
model_disease = RandomForestClassifier(n_estimators=100, random_state=42)
model_disease.fit(X_train, y_train_disease)

# Train age of death prediction model
model_age_of_death = RandomForestRegressor(n_estimators=100, random_state=42)
model_age_of_death.fit(X_train, y_train_age_of_death)

# Step 4: Digital Twin Development
def digital_twin(age, bmi, sex, smoker, region):
    # simulate individual's health outcomes using machine learning model
    input_data = pd.DataFrame({'age': [age], 'bmi': [bmi]})
    for var in X_train.columns:
        if var not in input_data.columns:
            input_data[var] = [0]
    
    # Set the correct values for the one-hot encoded columns
    if sex == 'Male':
        input_data['sex_Male'] = [1]
    elif sex == 'Female':
        input_data['sex_Female'] = [1]
    
    if smoker == 'Yes':
        input_data['smoker_Yes'] = [1]
    elif smoker == 'No':
        input_data['smoker_No'] = [1]
    
    if region == 'North':
        input_data['region_North'] = [1]
    elif region == 'South':
        input_data['region_South'] = [1]
    elif region == 'East':
        input_data['region_East'] = [1]
    elif region == 'West':
        input_data['region_West'] = [1]
    
    # Reorder the columns to match the training data
    input_data = input_data[X_train.columns]
    
    # Predict disease probability
    disease_prediction = model_disease.predict(input_data)
    
    # Predict age of death
    age_of_death_prediction = model_age_of_death.predict(input_data)
    
    return disease_prediction, age_of_death_prediction

# Step 5: Personalized Health Recommendations
def personalized_health_recommendations(disease_prediction, age_of_death_prediction):
    # provide personalized health recommendations based on disease prediction and age of death prediction
    if disease_prediction == 1:
        return f'High risk of disease. Consult a doctor. Predicted age of death: {int(age_of_death_prediction[0])}'
    else:
        return f'Low risk of disease. Maintain a healthy lifestyle. Predicted age of death: {int(age_of_death_prediction[0])}'

# Example usage:
age = 20
bmi = 25
sex = 'Female'
smoker = 'Yes'
region = 'North'
disease_prediction, age_of_death_prediction = digital_twin(age, bmi, sex, smoker, region)
health_recommendations = personalized_health_recommendations(disease_prediction, age_of_death_prediction)
print(f'Health recommendations: {health_recommendations}')