import streamlit as st
from prediction_helper import predict

title_name = 'Credit Risk Modelling'


st.set_page_config(page_title=title_name, layout='wide')
st.markdown('<style>div.block-container { padding-top: 3rem; padding-bottom: 1rem; } footer { display: none; }</style>', unsafe_allow_html=True)
st.title(title_name)

# 🔧 Field definitions
field_definitions = {
    'age': {'type': 'number', 'label': 'Age', 'default': 28, 'min': 0, 'max': 100, 'step': 1},
    'income': {'type': 'number', 'label': 'Income', 'default': 1200000, 'min': 0, 'max': 12_00_000, 'step': 10000},
    'loan_amount': {'type': 'number', 'label': 'Loan Amount', 'default': 2560000, 'min': 0, 'max': 25_60_000, 'step': 10000},
    'loan_to_income_ratio': {'type': 'derived', 'label': 'Loan to Income Ratio', 'default': '0'},  # special field (derived from loan_amount and income)
    'loan_tenure_months': {'type': 'number', 'label': 'Loan Tenure (in months)', 'default': 36, 'min': 0, 'max': 100, 'step': 1},
    'avg_dpd_per_delinquency': {'type': 'number', 'label': 'Average dpd per delinquency', 'default': 20, 'min': 0, 'max': 30, 'step': 1},
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

left_col, divider_col, right_col = st.columns([2, 0.05, 1])

with left_col:
    # Render 2 fields per row
    for start in range(0, len(items), 2):
        cols = st.columns(2)
        for col, (field_name, params) in zip(cols, items[start:start+2]):
            with col:
                ftype = params.get('type', 'number')

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
                        value = st.radio(
                            label=f'{params.get("label", field_name)}',
                            options=options,
                            index=index,
                            horizontal=True,
                            key=f'{field_name}_cat',
                        )
                    else:
                        value = None

                elif ftype == 'derived':
                    value = (user_inputs['loan_amount'] / user_inputs['income']) if user_inputs['income'] > 0 else 0
                    st.text_input(
                        label=f'{params.get("label", field_name)}  (auto-calculated)',
                        value=f'{value:.2f}',
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

with divider_col:
    st.markdown('<div style="border-left: 2px solid #e0e0e0; height: 100%; min-height: 400px;"></div>', unsafe_allow_html=True)

with right_col:
    st.subheader('Credit Risk Assessment')
    if st.button('Calculate Risk'):
        probability, credit_score, rating = predict(user_inputs)

        st.metric('Default Probability', f'{probability:.2%}')
        st.metric('Credit Score', credit_score)
        st.metric('Rating', rating)
