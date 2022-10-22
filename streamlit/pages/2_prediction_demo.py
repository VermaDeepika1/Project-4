import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
from io import StringIO
import pandas as pd
import pickle
import numpy as np

# st.set_page_config(page_title='Predictions!' )

st.title('Hospitalization Prediction Hah!')
st.sidebar.success("Lets click!")


X_train_dummies=pd.read_csv('./pages/models/X2_train_dummies.csv')
X_train_dummies=X_train_dummies.iloc[:,0]
X_train_dummies=list(X_train_dummies)



#filepath to our pickeled model
with open('./pages/models/demo_model_logreg2.pkl','rb') as pickle_model:
    model=pickle.load(pickle_model)

State = st.selectbox('Select your state',options= ['PA', 'MI', 'NJ', 'MO', 'LA', 'CO', 'TX',
'IA', 'IL', 'WA', 'OH','WI', 'MN', 'CT', 'SC', 'NY', 'VA', 'AL', 'NC', 'MA', 'NM', 'NV','CA',
'OK', 'AZ', 'NH', 'OR', 'TN', 'AR', 'MD', 'GA', 'ID', 'IN', 'FL', 'KS', 'UT', 'MT', 'KY', 'WY',
'ME', 'DC', 'VT', 'AK', 'HI'])

Age=st.selectbox('Select your age group',options= ['18 to 49 years', '65+ years', '50 to 64 years', '0 - 17 years'])

Gender=st.selectbox('Select your gender',options= ['Male','Female'])

Race=st.selectbox('Select your Race', options=['White', 'Black', 'Asian', 'American Indian/Alaska Native',
       'Multiple/Other', 'Native Hawaiian/Other Pacific Islander'])

Ethnicity=st.selectbox('Select your ethnicity', options=['Non-Hispanic/Latino', 'Hispanic/Latino'])

Month=st.selectbox('Select the month of the year', options=[1,2,3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

Symptom=st.selectbox('Are you Symptomatic?', options=['Symptomatic','Asymptomatic'])

#Add text to predcition
X=pd.DataFrame({'res_state': State, 'age_group': Age, 'sex': Gender, 'race': Race, 'ethnicity': Ethnicity, 'symptom_status':Symptom,'month':Month}, index=[0])
features=['res_state','age_group','sex','race','ethnicity','symptom_status','month']
#dummyfying columns:
df_dum=pd.get_dummies(data=X, drop_first=True)

#Removing additional dummy columns
for col in df_dum.columns:
    if ("_" in col) and (col.rsplit("_",1)[0] in features) and col not in X_train_dummies:
        # print("Removing additional feature {}".format(col))
        df_dum.drop(col, axis=1, inplace=True)

#Adding missing columns
for col in X_train_dummies:
    if col not in df_dum.columns:
        # print("Adding missing feature {}".format(col))
        df_dum[col] = 0

df_dum=df_dum[X_train_dummies]

if st.button('Predict'):
    predicted_hosp=model.predict(df_dum)
    hosp_prob=model.predict_proba(df_dum)
    #Write out your prediction
    st.write(f"Go to the Doctor? {'Yes' if predicted_hosp==1 else 'No'}")
    st.write(f'Probability of Hospitalization {np.round(hosp_prob[0][1],2)}')
