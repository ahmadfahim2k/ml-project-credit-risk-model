import streamlit as st
from prediction_helper import predict

title_name = 'Credit Risk Modelling'

st.set_page_config(page_title=title_name, layout='wide')
st.title(title_name)

# 🔧 Field definitions
field_definitions = {
    'age': {'type': 'number', 'label': 'Age', 'default': 28, 'min': 0, 'max': 100, 'step': 1},
    'income': {'type': 'number', 'label': 'Income', 'default': 1200000, 'min': 0, 'max': 12_00_000, 'step': 1000},
    'loan_amount': {'type': 'number', 'label': 'Loan Amount', 'default': 2560000, 'min': 0, 'max': 25_60_000, 'step': 1000},
    'loan_to_income_ratio': {'type': 'derived', 'label': 'Loan to Income Ratio', 'default': '0'},  # special field (derived from loan_amount and income)
    'loan_tenure_months': {'type': 'number', 'label': 'Loan Tenure (in months)', 'default': 36, 'min': 0, 'max': 100, 'step': 1},
    'avg_dpd_per_delinquency': {'type': 'number', 'label': 'Average dpd per delinquency', 'default': 20, 'min': 0, 'max': 30  , 'step': 1},
    'delinquency_ratio': {'type': 'number', 'label': 'Delinquency Ratio', 'default': 30, 'min': 0, 'max': 100, 'step': 1},
    'credit_utilization_ratio': {'type': 'number', 'label': 'Credit Utilization Ratio', 'default': 30, 'min': 0, 'max': 100, 'step': 1},
    'num_open_accounts': {'type': 'number', 'label': 'Number of open accounts', 'default': 2, 'min': 1, 'max': 4, 'step': 1},
    'residence_type': {'type': 'categorical', 'label': 'Residence Type', 'options': ['Owned', 'Rented', 'Mortgage'], 'default': 'Owned'},
    'loan_purpose': {'type': 'categorical', 'label': 'Loan Purpose', 'options': ['Education', 'Home', 'Auto', 'Personal'], 'default': 'Education'},
    'loan_type': {'type': 'categorical', 'label': 'Loan Type', 'options': ['Unsecured', 'Secured'], 'default': 'Unsecured'},
}

# ✅ Initialize fields dictionary with defaults
user_inputs = {name: params.get('default') for name, params in field_definitions.items()}

items = list(field_definitions.items())

# Render 3 fields per row
for start in range(0, len(items), 3):
    cols = st.columns(3)
    for col, (field_name, params) in zip(cols, items[start:start+3]):
        with col:
            print(f'params: {params}')
            ftype = params.get('type', 'number')
            # st.markdown(f'**{field_name}**')

            if ftype == 'number':
                value = st.number_input(
                    label=f'Enter {params.get("label", field_name)}',
                    min_value=params.get('min', None),
                    max_value=params.get('max', None),
                    value=user_inputs[field_name],
                    step=params.get('step', 1),
                    key=f'{field_name}_num',
                )

            elif ftype == 'categorical':
                options = params.get('options', [])
                default = user_inputs[field_name] or (options[0] if options else None)
                if options:
                    index = options.index(default) if default in options else 0
                    value = st.selectbox(
                        label=f'Select {params.get("label", field_name)}',
                        options=options,
                        index=index,
                        key=f'{field_name}_cat',
                    )
                else:
                    value = None

            elif ftype == 'derived':
                # placeholder — will update later dynamically
                value = st.text_input(
                    label=f'{params.get("label", field_name)}  (auto-calculated)',
                    value=user_inputs[field_name],
                    disabled=True,
                    key=f'{field_name}_derived',
                )

            else:
                st.warning(f'Unknown type for {field_name}, defaulting to number.')
                value = st.number_input(
                    label=f'Enter {field_name}',
                    value=0,
                    key=f'{field_name}_fallback',
                )

            # Update dictionary with user/derived values
            user_inputs[field_name] = value

# 🔄 Dynamically update loan_to_income_ratio
loan_to_income_ratio = (user_inputs['loan_amount'] / user_inputs['income']) if user_inputs['income'] > 0 else 0
user_inputs['loan_to_income_ratio'] = loan_to_income_ratio

# Force update UI for income_level (so it reflects computed value)
st.session_state['loan_to_income_ratio'] = user_inputs['loan_to_income_ratio']

st.subheader('fields (parameter values)')
st.json(user_inputs)

if st.button('Calculate Risk'):
    probability, credit_score, rating = predict(user_inputs)
    
    st.write(f"Default Probablity : {probability:.2%}")
    st.write(f"Credit Score : {credit_score}")
    st.write(f"Rating : {rating}")