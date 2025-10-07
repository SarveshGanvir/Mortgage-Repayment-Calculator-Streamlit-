import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Mortgage Repayment Calculator")

st.write("### Input Data")
col1,col2 = st.columns(2)
home_value = col1.number_input("Home value",min_value=0,value = 500000)
deposit = col1.number_input("Deposit",min_value=0,value = 100000)
interest_rate = col2.number_input("Interest Rate", min_value=0.0, value = 5.5)
loan_terms = col2.number_input("Loan Term(in yrs)",min_value=1,value = 30)

# calculations
loan_amount = home_value - deposit
monthly_interest_rate = (interest_rate / 100) / 12
no_of_months = loan_terms * 12
monthly_loan_amount = (
    (loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** no_of_months)
     / ((1 + monthly_interest_rate) ** no_of_months-1))
)

#Display repayment
total_payment = no_of_months * monthly_loan_amount
total_intrest = (total_payment - loan_amount)

st.write("### Repayment")
col1,col2,col3 = st.columns(3)
col1.metric(label="Monthly Repayment",value=f"${monthly_loan_amount:,.2f}")
col2.metric(label="Total Repayment",value=f"${total_payment:,.0f}")
col3.metric(label="Total intrest",value=f"${total_intrest:,.0f}")

# Create a data-frame with the payment schedule.
schedule = []
remaining_balance = loan_amount

for i in range(1, no_of_months + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_loan_amount - interest_payment
    remaining_balance -= principal_payment
    year = (i-1) //12 + 1  # Calculate the year into the loan
    schedule.append(
        [
            i,
            monthly_loan_amount,
            principal_payment,
            interest_payment,
            remaining_balance,
            year,
        ]
    )

df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
)

# Display the data-frame as a chart.
st.write("### Payment Schedule")
st.line_chart(df[["Month", "Remaining Balance"]].set_index("Month"))

