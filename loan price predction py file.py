# -*- coding: utf-8 -*-
"""Final project-Ayush kumar sahu-21DAT-079.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1v3w8VdwKdjlfT7Ze8Rpk4oqswGlahuRa

Data analysis and visualization
"""

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

from math import pi
import seaborn as sns

"""## classifier"""

from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import RandomForestClassifier

from sklearn.linear_model import LogisticRegression

"""## metrics"""

from sklearn.preprocessing import LabelEncoder

from sklearn.model_selection import train_test_split

from sklearn.metrics import confusion_matrix

from sklearn.metrics import classification_report

from sklearn.metrics import accuracy_score

"""# Data Preview"""

#load training and testing data

file_train ='/content/train_u6lujuX_CVtuZ9i.csv' 
file_test = '/content/test_Y3wMUE5_7gLdaTN.csv'
loan_train = pd.read_csv(file_train)
loan_test = pd.read_csv(file_test)

# preview data

loan_train.head()

loan_train_cc = loan_train.copy()

loan_train.columns

loan_test.columns

loan_train.dtypes

loan_train.describe()

len(loan_train)

len(loan_test)

# missing data
loan_train.isna().values.any()

# missing data
loan_test.isna().values.any()

# visualizing the missing data in the TEST data

import seaborn as sns

plt.figure(figsize=(10,6))
sns.displot(
    data=loan_train.isna().melt(value_name="missing"),
    y="variable",
    hue="missing",
    multiple="fill",
    aspect=1.25)

plt.show()

loan_train.isna().sum()

"""# Data Cleaning & Preparation"""

# doing a forward fill here, so, we get only 1 or 0 to fill the missing data

loan_train['Credit_History'].fillna(method='ffill', inplace=True)
loan_train['Credit_History'].isna().values.any()

# filling this column using the median of the values

median_loan = loan_train['Loan_Amount_Term'].median()
loan_train['Loan_Amount_Term'].fillna((median_loan), inplace=True)
loan_train['Loan_Amount_Term'].isna().values.any()

# filling this column using the median of the values

median_loan_amount = loan_train['LoanAmount'].median()
loan_train['LoanAmount'].fillna((median_loan_amount), inplace=True)
loan_train['LoanAmount'].isna().values.any()

# Counting the values to know which occurs most frequently
loan_train['Self_Employed'].value_counts()

#Filling with mode
loan_train['Self_Employed'].fillna('No', inplace=True)
loan_train['Self_Employed'].isna().values.any()

# filling with mode
loan_train['Dependents'].fillna(0, inplace=True)
loan_train['Dependents'].isna().values.any()

loan_train['Married'].mode()

# filling with mode
loan_train['Married'].fillna('Yes', inplace=True)
loan_train['Married'].isna().values.any()

loan_train['Gender'].mode()

# filling with mode
loan_train['Gender'].fillna('Male', inplace=True)
loan_train['Gender'].isna().values.any()

#runing a quick check
loan_train.isna().sum()

"""# After sorting the missing values for train data, I will do the same for test data"""

# A preview of missing data in the testing set

loan_test.isna().sum()

# filling in credit history
loan_test['Credit_History'].fillna(method='ffill', inplace=True)

# filling in loan amount term
median_loan_test = loan_test['Loan_Amount_Term'].median()
loan_test['Loan_Amount_Term'].fillna((median_loan_test), inplace=True)

# filling in loan amount
median_loan_amount_test = loan_test['LoanAmount'].median()
loan_test['LoanAmount'].fillna((median_loan_amount_test), inplace=True)

# filling in self employed
loan_test['Self_Employed'].fillna('No', inplace=True)

# filling in dependents
loan_test['Dependents'].fillna(0, inplace=True)

# filling in gender
loan_test['Gender'].fillna('Male', inplace=True)

loan_test.isna().values.any()

#runing a final check

loan_test.isna().sum()

"""#dealing with duplicate values"""

loan_train.duplicated().values.any()

loan_test.duplicated().values.any()

"""# Data Visualization & Exploratory Analysis"""

#previewing the data again

loan_train.head()

# Bar charts to get a high level view of categorical data

fig, ax = plt.subplots(3, 2, figsize=(16, 18))

loan_train.groupby(['Gender'])[['Gender']].count().plot.bar(
    color=plt.cm.Paired(np.arange(len(loan_train))), ax=ax[0,0])
loan_train.groupby(['Married'])[['Married']].count().plot.bar(
    color=plt.cm.Paired(np.arange(len(loan_train))), ax=ax[0,1])
loan_train.groupby(['Education'])[['Education']].count().plot.bar(
    color=plt.cm.Paired(np.arange(len(loan_train))), ax=ax[1,0])
loan_train.groupby(['Self_Employed'])[['Self_Employed']].count().plot.bar(
    color=plt.cm.Paired(np.arange(len(loan_train))), ax=ax[1,1])

loan_train.groupby(['Loan_Status'])[['Loan_Status']].count().plot.bar(
    color=plt.cm.Paired(np.arange(len(loan_train))),ax=ax[2,0])
loan_train.groupby(['Property_Area'])[['Loan_Status']].count().plot.bar(
    color=plt.cm.Paired(np.arange(len(loan_train))),ax=ax[2,1])

plt.show()

#passing all categorical columns into a list

categorical_columns = loan_train_cc.select_dtypes('object').columns.to_list()

# filtering the list to remove Loan_ID column which is not relevant to the analysis
categorical_columns[1:]

# looping through the list, and creating a chart for each

for i in categorical_columns[1:]: 
    plt.figure(figsize=(15,10))
    plt.subplot(3,2,1)
    sns.countplot(x=i ,hue='Loan_Status', data=loan_train_cc, palette='ocean')
    plt.xlabel(i, fontsize=14)

#Plot4- Scatterplot
fig, ax = plt.subplots(2,2, figsize=(14,12))

sns.scatterplot(data=loan_train,x="ApplicantIncome", y="LoanAmount",s=70, hue="Loan_Status", palette='ocean',ax=ax[0,0])
sns.histplot(loan_train, x=loan_train['LoanAmount'], bins=10, ax=ax[0,1])
sns.scatterplot(data=loan_train,x='CoapplicantIncome', y='LoanAmount',s=70, hue='Loan_Status',palette='ocean', ax=ax[1,0])
sns.scatterplot(data=loan_train,x='Loan_Amount_Term', y='LoanAmount', s=70, hue='Loan_Status',palette='ocean', ax=ax[1,1])

plt.show()

loan_train.corr()

"""# Let's get a more high level view of the correlations between numeric variables"""

#plotting correlation overview of the variables.

fig, ax = plt.subplots(figsize=(9, 7))
correlations = loan_train.corr()
  
# plotting correlation heatmap
dataplot = sns.heatmap(correlations, cmap="YlGnBu", annot=True)
  
# displaying heatmap
plt.show()

"""# Data Pre-processing for Model Building"""

#taking another preview of the data
loan_train.head()

#identifying all categorical columns & pass into a variable
objectlist_train = loan_train.select_dtypes(include = "object").columns

# Labeling Encoding for object to numeric conversion

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

for feature in objectlist_train:
    loan_train[feature] = le.fit_transform(loan_train[feature].astype(str))

print (loan_train.info())

# repeating the same process to encode the test data

objectlist_test = loan_test.select_dtypes(include='object').columns

for feature in objectlist_test:
    loan_test[feature] = le.fit_transform(loan_test[feature].astype(str))

print (loan_test.info())

#reruning correlation, with other numeric variables now added

fig, ax = plt.subplots(figsize=(10, 8))
correlations_ML = loan_train.iloc[:,1:].corr() # filer out the Loan_ID column as it is not relevant
sns.heatmap(correlations_ML, cmap="YlGnBu", annot=True)
plt.show()

"""# Machine Learning Model Development"""

x = loan_train.iloc[:,1:].drop('Loan_Status', axis=1) # droping loan_status column because that is what i am predicting
y = loan_train['Loan_Status']
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.30, random_state=0)

"""# Decision Tree Classifier Model"""

df_model = DecisionTreeClassifier()
df_model.fit(train_x, train_y)
predict_y = df_model.predict(test_x)
print(classification_report(test_y, predict_y))
print("Accuracy:", accuracy_score(predict_y, test_y))

"""# Random Forest Classifier"""

rf_model = RandomForestClassifier(n_estimators=100)
rf_model.fit(train_x, train_y)
predict_y_2 = rf_model.predict(test_x)
print(classification_report(test_y, predict_y_2))
print("Accuracy:", accuracy_score(predict_y_2, test_y))

"""# Logistic Regression Model"""

lr_model = LogisticRegression(solver='lbfgs', multi_class='auto')
lr_model.fit(train_x, train_y)
predict_y_3 = lr_model.predict(test_x)
print(classification_report(test_y, predict_y_3))
print("Accuracy:", accuracy_score(predict_y_3, test_y))

