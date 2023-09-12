import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier # Decision tree classifier
from sklearn.model_selection import train_test_split
import pickle

THRESHOLD = 488

# Read data from the Excel file into a pandas DataFrame
data = pd.read_excel('Data sheet.xlsx', sheet_name='Sheet1')

# Prepare the data
X = data[['DIM( Days In Milk)','Avg(7 days). Daily MY( L )', 'Kg. milk 305 ( Kg )', 'Fat (%)' , 'SNF (%)', 'Density ( Kg/ m3','Protein (%)','Conductivity (mS/cm)','pH','Freezing point (⁰C)','Salt (%)','Lactose (%)']]
y = data['SCC (103cells/ml)'].apply(lambda x: 1 if x > THRESHOLD else 0)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

import category_encoders as ce # Import the relevant library
encoder = ce.OrdinalEncoder(cols=['DIM( Days In Milk)','Avg(7 days). Daily MY( L )', 'Kg. milk 305 ( Kg )', 'Fat (%)' , 'SNF (%)', 'Density ( Kg/ m3','Protein (%)','Conductivity (mS/cm)','pH','Freezing point (⁰C)','Salt (%)','Lactose (%)'])
X_train = encoder.fit_transform(X_train)
X_test = encoder.transform(X_test)

# Create decision treeclassifier object
clf_gini = DecisionTreeClassifier(criterion='gini',max_depth=2,random_state=0) # Use the gini index as the criterion
clf_gini.fit(X_train, y_train) # Train the classifier

with open("model.pkl", "wb") as file:
    pickle.dump(clf_gini, file, protocol=4)