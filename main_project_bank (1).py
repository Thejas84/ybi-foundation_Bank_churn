# -*- coding: utf-8 -*-
"""main_project_bank.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1B_GMg1vUC4roVswXYcN9vITDb64yJZLs

# Bank Customer Churn Model

# Objective

1. **Prediction**: The primary objective is to predict which bank customers are at risk of leaving or churning in the near future.

2. **Retention**: To implement effective retention strategies for at-risk customers, thereby reducing churn rates and preserving the bank's customer base.

3. **Customer Satisfaction**: Enhance overall customer satisfaction by addressing issues leading to churn and improving customer experiences.

4. **Cost Reduction**: Optimize marketing and resource allocation by focusing efforts on customers most likely to churn, reducing unnecessary expenses.

5. **Financial Stability**: Ultimately, the model aims to contribute to the bank's financial stability by preserving revenue streams and long-term customer relationships.

#Data Source

1. **Customer Data**
2. **CRM Records**
3. **Transaction Logs**
4. **Customer Surveys**
5. **Call Center Data**
6. **External Sources**

# import library
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""# Import Data"""

df = pd.read_csv("https://github.com/YBI-Foundation/Dataset/raw/main/Bank%20Churn%20Modelling.csv")

"""#Analysis Data"""

df.head()

df.tail()

df.info()

df.duplicated('CustomerId').sum()

df = df.set_index('CustomerId')

df.info()

"""#Encoding"""

df['Geography'].value_counts()

df.replace({'Geography':{'France':2, 'Germany':1, 'Spain': 0}},inplace = True)

df['Gender'].value_counts()

df.replace({'Gender':{'Male':0, 'Female':1}},inplace = True)

df['Num Of Products'].value_counts()

df.replace({'Num Of Products': {1:0, 2:1, 3:1, 4:1 }}, inplace = True)

df['Has Credit Card'].value_counts()

df['Is Active Member'].value_counts()

df.loc[(df['Balance']==0), 'Churn'].value_counts()

df['Zero Balance'] = np.where(df['Balance']>0, 1, 0)

df['Zero Balance'].hist()

df.groupby(['Churn', 'Geography']).count()

"""# Define Lable and features"""

df.columns

X = df.drop(['Surname','Churn'], axis = 1)

y = df['Churn']

X.shape, y.shape

df['Churn'].value_counts()

sns.countplot(x = 'Churn', data = df);

X.shape, y.shape

"""##Random Under Sampling"""

from imblearn.under_sampling import RandomUnderSampler

rus = RandomUnderSampler(random_state = 2529)

X_rus, y_rus = rus.fit_resample(X, y)

X_rus.shape, y_rus.shape, X.shape, y.shape

y.value_counts()

y_rus.value_counts()

y_rus.value_counts()

y_rus.plot(kind = 'hist')

"""##Random Over Sampling"""

from imblearn.over_sampling import RandomOverSampler

ros = RandomOverSampler(random_state= 2529)

X_ros, y_ros = ros.fit_resample(X, y)

y.value_counts(0)

y_ros.plot(kind = 'hist')

"""##Train Test Split"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 2529, test_size = 0.3)

X_train

X_test

#Split Random under Sample Data
X_train_rus, X_test_rus, y_train_rus, y_test_rus = train_test_split(X, y, random_state = 2529, test_size = 0.3)

#Split Random Over Sample Data
X_train_ros, X_test_ros, y_train_ros, y_test_ros = train_test_split(X_ros, y_ros , test_size=0.3 ,random_state=2529)

"""#Standardize Feature"""

from sklearn.preprocessing import StandardScaler

sc = StandardScaler()

"""#Standardize Original Data"""

X_train[['CreditScore' , 'Age', 'Tenure', 'Balance', 'Estimated Salary']] = sc.fit_transform(X_train[['CreditScore' , 'Age', 'Tenure', 'Balance', 'Estimated Salary']])

X_test[['CreditScore' , 'Age', 'Tenure', 'Balance', 'Estimated Salary']] = sc.fit_transform(X_test[['CreditScore' , 'Age', 'Tenure', 'Balance', 'Estimated Salary']])

"""#Standardize Random Under Sample Data"""



X_train_rus[['CreditScore' , 'Age', 'Tenure', 'Balance', 'Estimated Salary']] = sc.fit_transform(X_train_rus[['CreditScore' , 'Age', 'Tenure', 'Balance', 'Estimated Salary']])

X_test_rus[['CreditScore' , 'Age', 'Tenure', 'Balance', 'Estimated Salary']] = sc.fit_transform(X_test_rus[['CreditScore' , 'Age', 'Tenure', 'Balance', 'Estimated Salary']])

"""#Standardize Random Over Sample Data"""

X_train_ros[['CreditScore' , 'Age', 'Tenure', 'Balance', 'Estimated Salary']] = sc.fit_transform(X_train_ros[['CreditScore' , 'Age', 'Tenure', 'Balance', 'Estimated Salary']])

X_test_ros[['CreditScore' , 'Age', 'Tenure', 'Balance', 'Estimated Salary']] = sc.fit_transform(X_test_ros[['CreditScore' , 'Age', 'Tenure', 'Balance', 'Estimated Salary']])

"""#Support Vector Machine Classifier"""

from sklearn.svm import SVC

svc = SVC()

svc.fit(X_train, y_train)

y_pred = svc.predict(X_test)

"""# Model Accuracy"""

from sklearn.metrics import  confusion_matrix, classification_report

confusion_matrix(y_test, y_pred)

print(classification_report(y_test, y_pred))

"""##Hyperparameter Tunning"""

from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

param_grid = {
    'C': [0.1, 1, 10],
    'gamma': [1, 0.1, 0.01],
    'kernel': [ 'rbf'],
    'class_weight': ['balanced'],
}

grid = GridSearchCV(SVC(), param_grid, refit=True, verbose=2, cv=2)
grid.fit(X_train, y_train)

print(grid.best_estimator_)

grid_predictions = grid.predict(X_test)

confusion_matrix(y_test , grid_predictions)

print(classification_report(y_test, grid_predictions))

"""##Model with Random Under Sampling


"""

svc_rus = SVC()

svc_rus.fit(X_train_rus, y_train_rus)

y_pred_rus = svc_rus.predict(X_test_rus)

"""##Model Accuracy"""

confusion_matrix(y_test_rus, y_pred_rus)

print(classification_report(y_test_rus, y_pred_rus))

"""#hyperparameter Tunning"""

param_grid = {
    'C': [0.1, 1, 10],
    'gamma': [1, 0.1, 0.01],
    'kernel': [ 'rbf'],
    'class_weight': ['balanced'],
}

grid_rus = GridSearchCV(SVC(), param_grid, refit=True, verbose=2, cv=2)
grid_rus.fit(X_train_rus, y_train_rus)

print(grid_rus.best_estimator_)

grid_predictions_rus = grid_rus.predict(X_test_rus)

confusion_matrix(y_test_rus, grid_predictions_rus )

print(classification_report(y_test_rus, grid_predictions_rus))

"""##Model with Random Over Sampling

"""

svc_ros = SVC()

svc_ros.fit(X_train_ros, y_train_ros)

y_pred_ros = svc_ros.predict(X_test_ros)

"""## *Model* Accuracy"""

confusion_matrix(y_test_ros, y_pred_ros)

print(classification_report(y_test_ros, y_pred_ros))

"""#hyperparameter Tunning

"""

param_grid = {
    'C': [0.1, 1, 10],
    'gamma': [1, 0.1, 0.01],
    'kernel': [ 'rbf'],
    'class_weight': ['balanced'],
}

grid_ros = GridSearchCV(SVC(), param_grid, refit=True, verbose=2, cv=2)
grid_ros.fit(X_train_ros, y_train_ros)

print(grid_ros.best_estimator_)

grid_predictions_ros = grid_ros.predict(X_test_ros)

confusion_matrix(y_test_ros, grid_predictions_ros)

print(classification_report(y_test_ros, grid_predictions_ros))

"""#Lets Compare"""

print(classification_report(y_test, y_pred))

print(classification_report(y_test, grid_predictions))

print(classification_report(y_test_rus, y_pred_rus))

print(classification_report(y_test_rus, grid_predictions_rus))

print(classification_report(y_test_ros, grid_predictions_ros))

"""# Explaination

A Bank Customer Churn Model is a predictive analytics tool used by banks and financial institutions to forecast and address customer churn, which is when customers discontinue their engagement with a bank's services or close their accounts. Here's an in-depth explanation of this model:

**1. **Churn Definition**: Customer churn, also known as attrition or customer turnover, occurs when a customer ceases to use a bank's products or services, leading to a potential loss of revenue and customer base.

**2. **Data Collection**: The model relies on data from various sources, including customer databases, CRM systems, transaction records, customer surveys, call center logs, and external sources such as economic indicators and competitor data.

**3. **Data Preprocessing**: Data is cleaned, organized, and prepared for analysis. This step includes handling missing values, standardizing data formats, and ensuring data privacy and security compliance.

**4. **Feature Engineering**: Relevant features or variables are selected or created from the data to build predictive models. These features can include customer demographics, transaction history, customer feedback, and more.

**5. **Model Building**: Machine learning and statistical techniques are applied to build predictive models that assess the likelihood of a customer churning. Common algorithms include logistic regression, decision trees, random forests, and neural networks.

**6. **Model Training**: The model is trained on historical data that includes information about customers who have churned and those who have not. This training allows the model to learn patterns and relationships in the data.

**7. **Predictive Scoring**: Once trained, the model can assign churn probabilities to current customers. This score indicates the likelihood that a particular customer will churn in the future.

**8. **Risk Segmentation**: Customers are often segmented based on their churn risk scores. High-risk customers are prioritized for retention efforts, as they are more likely to churn and represent a greater potential loss to the bank.

**9. **Retention Strategies**: The bank uses insights from the model to develop personalized retention strategies for at-risk customers. These strategies may include targeted offers, improved customer service, or engagement initiatives.

**10. **Monitoring and Feedback**: The model's performance is continuously monitored, and its predictions are evaluated against real-world outcomes. Feedback loops are established to refine the model and improve retention strategies over time.

**11. **Cost Reduction**: By identifying high-risk customers and focusing retention efforts on them, the bank can optimize resource allocation and reduce the overall cost of customer retention.

**12. **Financial Impact**: The ultimate goal is to reduce customer churn, retain valuable customers, and maintain or increase the bank's revenue and profitability.

In summary, a Bank Customer Churn Model is a data-driven approach to reduce customer attrition by predicting which customers are most likely to churn and implementing targeted strategies to retain them. It combines data analytics, machine learning, and customer relationship management to enhance customer satisfaction and financial stability for the bank.
"""