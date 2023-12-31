# import the libraries (streamit, pandas, pickle)
import streamlit as st
import pandas as pd
import pickle


# import the pickled model and scaler
pickled_model = pickle.load(open('model.pkl', 'rb'))
pickled_scaler = pickle.load(open('scaler.pkl', 'rb'))


# create header for the streamlit app
st.title('Does one survived from Titantic? :ship:')
st.caption(
    'This model is trained to predict the survival of the passenger survived from Titanic.')
st.subheader('Fill in the form below to initiate the prediction.')


# Create a form for user input
form = st.form(key='my-form')


# Create the rows according to the features needed for the form.
# Name
Name = form.text_input('Name')
# First feature : Pclass
Pclass = form.selectbox(
    'Passenger Class [1st = Upper,2nd = Middle,3rd = Lower]', options=[1, 2, 3])
# Second feature : Sex
sex = form.selectbox('Sex', options=['Male', 'Female'])
# Third feature : Age
Age = form.number_input('Age', min_value=1, max_value=100, value=1, step=1)
# Fourth feature : number of siblings/spouses aboard the Titanic
SibSp = form.number_input('Number of siblings/spouses aboard the Titanic',
                          min_value=0, max_value=10, value=0, step=1)
# Fifth feature : number of parents/children aboard the Titanic
Parch = form.number_input('Number of parents/children aboard the Titanic',
                          min_value=0, max_value=10, value=0, step=1)
# Sixth feature :
embarked = form.selectbox('Port of Embarkation', options=[
                          'Cherbourg', 'Queenstown', 'Southampton'])
predict = form.form_submit_button('Predict')



# Make prediction based on user input
if predict:
    # convert sex to 0 and 1
    Sex = 0 if sex == "Male" else 1
    embarked_dict = {"Cherbourg": 0, "Queenstown": 1, "Southampton": 2}
    Embarked = embarked_dict[embarked]
    row = [Pclass, Sex, Age, SibSp, Parch, Embarked]
    columns = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Embarked']
    row_df = pd.DataFrame([row], columns=columns)
    # use transform instead of fit_transform
    normalized_row = pickled_scaler.transform(row_df.values)
    prediction = pickled_model.predict(normalized_row)
    st.subheader("Prediction Result")
    if prediction == 0:
        st.error(f'{Name} did not survive', icon="🚨")
    else:
        st.success(f'{Name} survived', icon="✅")


# Display the prediction result
