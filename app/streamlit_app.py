import streamlit as st
import pickle
import joblib
import pandas as pd
from zipfile import ZipFile
import os
from src import transform_resp
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title='Credit Risk Analyzer', page_icon='💳', layout='wide',
                   initial_sidebar_state='auto', menu_items={
                        # 'Get Help': None,
                        # 'Report a bug': None
     })

path = os.path.dirname(__file__)
folder_path = os.path.join(path,'../models')

# @st.cache(allow_output_mutation=True)
@st.cache_resource
def unzip_load(name):
    path_zip = os.path.join(path,'../models/'+name+'.zip')
    ZipFile(path_zip).extractall(folder_path)
    path_obj = os.path.join(path,'../models/'+name+'.joblib')
    # # return  pickle.load(open(path_obj, 'rb'))
    return  joblib.load(open(path_obj, 'rb'))

scaler = unzip_load('scaler2')
model = unzip_load('model2')

# age_default = None
# annual_income_default = 0.00
# accounts_default = 0
# credit_cards_default = 0
# delayed_payments_default = 0
# credit_card_ratio_default = 0.00
# emi_monthly_default = 0.00
# credit_history_default = 0
# loans_default = None
# missed_payment_default = 0
# minimum_payment_default = 0

st.title('Credit Risk Analyzer')
# st.caption('Made by Sahil')

st.markdown('''
            Click `>` if you don't see the sidebar. Fill out the form and click on **`ANALYZE`** to see your credit score.

            Or if you prefer, you can set random values by clicking on **`Generate Random Profile`**.
''')

import random

# Define a function to generate random profile values
def generate_random_profile():
    age = random.randint(18, 70)
    annual_income = round(random.uniform(15000.00, 100000.00), 2)
    accounts = random.randint(0, 5)
    credit_cards = random.randint(1, 10)
    delayed_payments = random.randint(0, 10)
    credit_card_ratio = round(random.uniform(0.00, 50.00), 2)
    emi_monthly = round(random.uniform(0.00, 1000.00), 2)
    credit_history = random.randint(0, 360)
    loans = random.sample(['Student Loan', 'Auto Loan', 'Mortgage Loan', 'Personal Loan', 'Home Equity Loan'], k=random.randint(1, 3))
    missed_payment = random.choice(['Yes', 'No'])
    minimum_payment = random.choice(['Yes', 'No'])

    return age, annual_income, accounts, credit_cards, delayed_payments, credit_card_ratio, emi_monthly, credit_history, loans, missed_payment, minimum_payment


# Initialize session state variables
if 'age_default' not in st.session_state:
    st.session_state.age_default = 18
    st.session_state.annual_income_default = 15000.00
    st.session_state.accounts_default = 0
    st.session_state.credit_cards_default = 10
    st.session_state.delayed_payments_default = 5
    st.session_state.credit_card_ratio_default = 43.00
    st.session_state.emi_monthly_default = 0.00
    st.session_state.credit_history_default = 4
    st.session_state.loans_default = ['Student Loan']
    st.session_state.missed_payment_default = 'No'
    st.session_state.minimum_payment_default = 'No'

# Button to generate random profile
if st.button('Generate Random Profile'):
    (st.session_state.age_default, st.session_state.annual_income_default, st.session_state.accounts_default, 
     st.session_state.credit_cards_default, st.session_state.delayed_payments_default, st.session_state.credit_card_ratio_default,
     st.session_state.emi_monthly_default, st.session_state.credit_history_default, st.session_state.loans_default, 
     st.session_state.missed_payment_default, st.session_state.minimum_payment_default) = generate_random_profile()

    # # Display the profile values
    # st.write(f"Age: {age_default}")
    # st.write(f"Annual Income: ${annual_income_default:,.2f}")
    # st.write(f"Number of Accounts: {accounts_default}")
    # st.write(f"Number of Credit Cards: {credit_cards_default}")
    # st.write(f"Number of Delayed Payments: {delayed_payments_default}")
    # st.write(f"Credit Card Ratio: {credit_card_ratio_default:.2f}")
    # st.write(f"EMI Monthly: ${emi_monthly_default:.2f}")
    # st.write(f"Credit History (Months): {credit_history_default}")
    # st.write(f"Loans: {', '.join(loans_default)}")
    # st.write(f"Missed Payments: {missed_payment_default}")
    # st.write(f"Minimum Payment: {minimum_payment_default}")


with st.sidebar:
    st.header('Credit Score Form')
    age = st.slider('What is your age?', min_value=18, max_value=100, step=1, value=st.session_state.age_default)
    annual_income = st.number_input('What is your Annual Income?', min_value=0.00, max_value=300000.00, value=st.session_state.annual_income_default)
    accounts = st.number_input('How many bank accounts do you have?', min_value=0, max_value=20, step=1, value=st.session_state.accounts_default)
    credit_cards = st.number_input('How many credit cards do you have?', min_value=0, max_value=12, step=1, value=st.session_state.credit_cards_default)
    delayed_payments = st.number_input('How many delayed payments do you have?', min_value=0, max_value=20, step=1, value=st.session_state.delayed_payments_default)
    credit_card_ratio = st.slider('What is your credit card utilization ratio?', min_value=0.00, max_value=100.00, value=st.session_state.credit_card_ratio_default)
    emi_monthly = st.number_input('How much EMI do you pay monthly?', min_value=0.00, max_value=5000.00, value=st.session_state.emi_monthly_default)
    credit_history = st.number_input('How many months old is your credit history?', min_value=0, max_value=500, step=1, value=st.session_state.credit_history_default)
    loans = st.multiselect('Which loans do you have?', ['Auto Loan', 'Credit-Builder Loan', 'Personal Loan',
                                                'Home Equity Loan', 'Mortgage Loan', 'Student Loan',
                                                'Debt Consolidation Loan', 'Payday Loan'], default=st.session_state.loans_default)
    
    # Ensure default values are valid
    valid_choices = ['Yes', 'No']
    missed_payment_default = st.session_state.missed_payment_default if st.session_state.missed_payment_default in valid_choices else 'No'
    minimum_payment_default = st.session_state.minimum_payment_default if st.session_state.minimum_payment_default in valid_choices else 'No'
    
    # Convert string values to their corresponding index for the radio buttons
    missed_payment_index = valid_choices.index(missed_payment_default)
    minimum_payment_index = valid_choices.index(minimum_payment_default)
    
    missed_payment = st.radio('Have you missed any payments in the last 12 months?', valid_choices, index=missed_payment_index)
    minimum_payment = st.radio('Have you paid the minimum amount on at least one of your credit cards?', valid_choices, index=minimum_payment_index)

    run = st.button('ANALYZE')

st.header('Credit Score Results')

col1, col2 = st.columns([3, 2])

with col2:
    x1 = [0, 6, 0]
    x2 = [0, 4, 0]
    x3 = [0, 2, 0]
    y = ['0', '1', '2']

    f, ax = plt.subplots(figsize=(5,2))

    p1 = sns.barplot(x=x1, y=y, color='#3EC300')
    p1.set(xticklabels=[], yticklabels=[])
    p1.tick_params(bottom=False, left=False)
    p2 = sns.barplot(x=x2, y=y, color='#FAA300')
    p2.set(xticklabels=[], yticklabels=[])
    p2.tick_params(bottom=False, left=False)
    p3 = sns.barplot(x=x3, y=y, color='#FF331F')
    p3.set(xticklabels=[], yticklabels=[])
    p3.tick_params(bottom=False, left=False)

    plt.text(0.7, 1.05, "POOR", horizontalalignment='left', size='medium', color='white', weight='semibold')
    plt.text(2.5, 1.05, "REGULAR", horizontalalignment='left', size='medium', color='white', weight='semibold')
    plt.text(4.7, 1.05, "GOOD", horizontalalignment='left', size='medium', color='white', weight='semibold')

    ax.set(xlim=(0, 6))
    sns.despine(left=True, bottom=True)

    # figure = st.pyplot(f, width=5)
    figure = st.pyplot(f)

with col1:
    placeholder = st.empty()

    if run:
        resp = {
            'age': age,
            'annual_income': annual_income,
            'accounts': accounts,
            'credit_cards': credit_cards,
            'delayed_payments': delayed_payments,
            'credit_card_ratio': credit_card_ratio,
            'emi_monthly': emi_monthly,
            'credit_history': credit_history,
            'loans': loans,
            'missed_payment': missed_payment,
            'minimum_payment': minimum_payment
        }
        output = transform_resp(resp)
        output = pd.DataFrame(output, index=[0])

        scaled_values = scaler.transform(output)
        output.loc[:,:] = scaled_values
        credit_score = model.predict(output)[0]

        if credit_score == 1:
            # st.balloons()
            t1 = plt.Polygon([[5, 0.5], [5.5, 0], [4.5, 0]], color='black')
            placeholder.markdown('Your credit score is **GOOD**! Congratulations!')
            st.markdown('This credit score indicates that this person is likely to repay a loan, so the risk of giving them credit is low.')
        elif credit_score == 0:
            t1 = plt.Polygon([[3, 0.5], [3.5, 0], [2.5, 0]], color='black')
            placeholder.markdown('Your credit score is **REGULAR**.')
            st.markdown('This credit score indicates that this person is likely to repay a loan, but can occasionally miss some payments. Meaning that the risk of giving them credit is medium.')
        elif credit_score == -1:
            t1 = plt.Polygon([[1, 0.5], [1.5, 0], [0.5, 0]], color='black')
            placeholder.markdown('Your credit score is **POOR**.')
            st.markdown('This credit score indicates that this person is unlikely to repay a loan, so the risk of lending them credit is high.')
        plt.gca().add_patch(t1)
        figure.pyplot(f)
        prob_fig, ax = plt.subplots()

        with st.expander('Click to see how certain the algorithm was'):
            plt.pie(model.predict_proba(output)[0], labels=['Poor', 'Regular', 'Good'], autopct='%.0f%%')
            st.pyplot(prob_fig)
        
        with st.expander('Click to see how much each feature weight'):
            importance = model.feature_importances_
            importance = pd.DataFrame(importance)
            columns = pd.DataFrame(['Age', 'Annual_Income', 'Num_Bank_Accounts',
                                    'Num_Credit_Card', 'Num_of_Delayed_Payment',
                                    'Credit_Utilization_Ratio', 'Total_EMI_per_month',
                                    'Credit_History_Age_Formated', 'Auto_Loan',
                                    'Credit-Builder_Loan', 'Personal_Loan', 'Home_Equity_Loan',
                                    'Mortgage_Loan', 'Student_Loan', 'Debt_Consolidation_Loan',
                                    'Payday_Loan', 'Missed_Payment_Day', 'Payment_of_Min_Amount_Yes'])

            importance = pd.concat([importance, columns], axis=1)
            importance.columns = ['importance', 'index']
            importance_fig = round(importance.set_index('index')*100.00, 2)
            loans = ['Auto_Loan', 'Credit-Builder_Loan', 'Personal_Loan', 
                    'Home_Equity_Loan', 'Mortgage_Loan', 'Student_Loan',
                    'Debt_Consolidation_Loan', 'Payday_Loan']

            # summing the loans
            Loans = importance_fig.loc[loans].sum().reset_index()
            Loans['index'] = 'Loans'
            Loans.columns=['index','importance']
            importance_fig = importance_fig.drop(loans, axis=0).reset_index()
            importance_fig = pd.concat([importance_fig, Loans], axis=0)
            importance_fig.sort_values(by='importance', ascending=True, inplace=True)

            # plotting the figure
            importance_figure, ax = plt.subplots()
            bars = ax.barh('index', 'importance', data=importance_fig)
            ax.bar_label(bars)
            plt.ylabel('')
            plt.xlabel('')
            plt.xlim(0,20)
            sns.despine(right=True, top=True)
            st.pyplot(importance_figure)