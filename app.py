import streamlit as st
import pickle
import numpy as np

def load_model():
    model_path = "model_files/model.pkl"
    loaded_model = pickle.load(open(model_path, 'rb'))
    return loaded_model

def prepare_data(gender,married, dependents, education,
                self_employed, loan_amount, loan_amount_term,
                credit_history, total_income, property_type):
    property_type_ohe = [0, 0]
    if (property_type == "Semi-Urban"):
        property_type_ohe[0] = 1
    elif property_type == "Urban":
        property_type_ohe[1] = 1

    gender = 1 if gender == "Yes" else 0
    married = 1 if married == "Yes" else 0
    self_employed = 1 if self_employed == "Yes" else 0
    credit_history = 1 if credit_history == "Yes" else 0
    education = 1 if education == "Graduate" else 0

    dependents = int(dependents.split('+')[0])

    total_income_by_loanAmt = (total_income/ loan_amount) ** 2
    loan_amount_term_by_amt = loan_amount / loan_amount_term

    X = [gender, married, dependents, education, self_employed, loan_amount, loan_amount_term,
         credit_history, total_income] + property_type_ohe + [total_income_by_loanAmt, loan_amount_term_by_amt]

    X = np.array([X])

    return X

def predict(gender,	married, dependents, education,
            self_employed, loan_amount, loan_amount_term,
            credit_history, total_income, property_type):

    X = prepare_data(gender,	married, dependents, education,
                                                self_employed, loan_amount, loan_amount_term,
                                                credit_history, total_income, property_type)

    model = load_model()
    pred = model.predict(X)
    if pred==1:
        result = "Your Loan Will Be Approved"
    else:
        result = "Your Loan will NOT Be Approved"
    st.markdown("**"+result+"**")
    st.write("Caution: The above result may not be correct, Kindly confirm with your bank.")

def display_details(gender,	married, dependents, education,
            self_employed, loan_amount, loan_amount_term,
            credit_history, total_income, property_type):
    X = [gender, married, dependents, education, self_employed, loan_amount, loan_amount_term,
         credit_history, total_income, property_type]
    st.write(X)

st.title("Loan Status Prediction")
st.image("images/LoanStatus.jpg", width=500)
col1, col2, col3 = st.columns(3)
with col1:
    loan_amount = st.number_input("Enter Loan Amount (In Thousands)",value=10)
    dependents = st.selectbox("Total Number of dependents", ('0', '1', '2', '3', '3+'))
    education = st.radio("Education", ("Graduate", "Under-Graduate"))
    married = st.radio("Married", ("Yes", "No"))
with col2:
    total_income = st.number_input("Enter Total Income (In Thousands)",value=200)
    self_employed = st.radio("Self-Emplyed", ("Yes", "No"))
    property_type = st.selectbox("Property Type", ("Rural", "Semi-Urban", "Urban"))
with col3:
    loan_amount_term = st.number_input("Enter Loan Amount Term (In Months)", value=12)
    gender = st.radio("Gender", ("Male", 'Female'))
    credit_history = st.radio("Credit History meets the criteria", ("Yes", "No"))

predict(gender,	married, dependents, education,
           self_employed, loan_amount, loan_amount_term,
           credit_history, total_income, property_type)
