import streamlit as st # type: ignore
import pandas as pd # type: ignore

# Load CSV files
df_provider = pd.read_csv('provider_mapping.csv')
df_operating = pd.read_csv('OperatingPhysician_mapping.csv')
df_other = pd.read_csv('OtherPhysician_mapping.csv')
df_attending = pd.read_csv('AttendingPhysician_mapping.csv')

# Title of the app
st.title('Provider ID Lookup')
selected_state = st.number_input('Select a State (from 1 to 54):', min_value=1, max_value=54, step=1)
selected_village = st.number_input('Select a Village (from 1 to 999):', min_value=1, max_value=999, step=1)
# Radio button group for selecting gender
gender = st.radio('Select Gender:', ['Male', 'Female'])

# Define the race options
race_options = [1, 2, 3, 5]

# Title of the app
st.title('Race Selection')

# Radio button group for selecting race
selected_race = st.radio('Select Race:', race_options)

# Text inputs for entering text data
# Text inputs for entering integer data
insc_claim_amt_reimbursed = st.text_input('InscClaimAmtReimbursed (integer):')
deductible_amt_paid = st.text_input('DeductibleAmtPaid (integer):')
no_of_months_part_a_cov = st.text_input('NoOfMonths_PartACov:')
no_of_months_part_b_cov = st.text_input('NoOfMonths_PartBCov:')
chronic_cond_alzheimer = st.text_input('ChronicCond_Alzheimer:')
chronic_cond_diabetes = st.text_input('ChronicCond_Diabetes:')
ip_annual_reimbursement_amt = st.text_input('IPAnnualReimbursementAmt:')
ip_annual_deductible_amt = st.text_input('IPAnnualDeductibleAmt:')
op_annual_reimbursement_amt = st.text_input('OPAnnualReimbursementAmt:')
op_annual_deductible_amt = st.text_input('OPAnnualDeductibleAmt:')


# Map selected gender to integer
gender_code = 1 if gender == 'Male' else 2
# Dropdown menu for selecting a provider from Provider category
selected_provider_provider = st.selectbox('Select a Provider:', df_provider['Provider'].unique())
provider_id_provider = df_provider[df_provider['Provider'] == selected_provider_provider]['Provider_ID'].values[0]

# Dropdown menu for selecting a provider from OperatingPhysician category
selected_provider_operating = st.selectbox('Select an Operating Physician:', df_operating['OperatingPhysician'].unique())
provider_id_operating = df_operating[df_operating['OperatingPhysician'] == selected_provider_operating]['OperatingPhysician_ID'].values[0]

# Dropdown menu for selecting a provider from OtherPhysician category
selected_provider_other = st.selectbox('Select an Other Physician:', df_other['OtherPhysician'].unique())
provider_id_other = df_other[df_other['OtherPhysician'] == selected_provider_other]['OtherPhysician_ID'].values[0]

# Dropdown menu for selecting a provider from AttendingPhysician category
selected_provider_attending = st.selectbox('Select an Attending Physician:', df_attending['AttendingPhysician'].unique())
provider_id_attending = df_attending[df_attending['AttendingPhysician'] == selected_provider_attending]['AttendingPhysician_ID'].values[0]

# Define the chronic conditions
chronic_conditions = [
    'Heart Failure',
    'Kidney Disease',
    'Cancer',
    'Obstructive Pulmonary Disease',
    'Depression',
    'Diabetes',
    'Ischemic Heart Disease',
    'Osteoporosis',
    'Rheumatoid Arthritis',
    'Stroke'
]

yob = st.text_input('Year of Birth:')
yod = st.text_input('Year of Death:')

# Create a dictionary to store the selected values
selected_values = {}

# Display radio buttons for each chronic condition and save the values in the dictionary
for condition in chronic_conditions:
    selected_values[condition] = st.radio(f'{condition}:', [0, 1], key=condition)



#from joblib import load # type: ignore

# Load the trained models
#sgd_model = load('sgd_model.joblib')
sgd_model = load('logreg_model.joblib')


# Now you can use the loaded models for predictions
# Extract values based on the order of the variables
values = [
    int(insc_claim_amt_reimbursed),
    float(deductible_amt_paid),
    gender_code,
    selected_race,
    int(selected_state),
    int(selected_village),
    int(no_of_months_part_a_cov),
    int(no_of_months_part_b_cov),
    int(chronic_cond_alzheimer),
    selected_values['Heart Failure'],
    selected_values['Kidney Disease'],
    selected_values['Cancer'],
    selected_values['Obstructive Pulmonary Disease'],
    selected_values['Depression'],
    selected_values['Diabetes'],
    selected_values['Ischemic Heart Disease'],
    selected_values['Osteoporosis'],
    selected_values['Rheumatoid Arthritis'],
    selected_values['Stroke'],
    int(ip_annual_reimbursement_amt),
    int(ip_annual_deductible_amt),
    int(op_annual_reimbursement_amt),
    int(op_annual_deductible_amt),
    provider_id_provider,
    provider_id_attending,
    provider_id_operating,
    provider_id_other,
    int(yob),
    int(yod)]  
# Predict using the loaded SGD model
predicted_value = sgd_model.predict([values])

# Check if predicted value is 1
if predicted_value == 1:
    # Display "Fraud Detected" in red color
    st.markdown("<p style='color:red;'>Fraud Detected</p>", unsafe_allow_html=True)
else:
    # Display "No Fraud Detected" in green color
    st.markdown("<p style='color:green;'>No Fraud Detected</p>", unsafe_allow_html=True)
