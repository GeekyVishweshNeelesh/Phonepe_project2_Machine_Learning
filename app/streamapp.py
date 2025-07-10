import pandas as pd
import streamlit as st
import plotly.express as px


# ------------------ SIDEBAR DASHBOARD SELECTION ------------------
# Set page config
st.set_page_config(page_title="📊 PhonePe Dashboard", layout="wide")

# Custom style to increase font size of radio button labels
st.markdown("""
    <style>
    .stRadio > div > label {
        font-size: 18px;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# Dashboard Selection - In desired order
page = st.radio(
    "📂 **Select a Dashboard to Explore**",
    [
        "Transaction Analysis",
        "Device Brand Usage",
        "Insurance Analysis (State-level)",
        "User Engagement (District-level)",
        "Transaction Analysis (District-level)",
        "Insurance Analysis (District-level)"
    ],
    index=0
)


# ------------------ TRANSACTION DASHBOARD ------------------
if page == "Transaction Analysis":
    st.title("📈 PhonePe Transaction Analysis")

    try:
        agg_txn = pd.read_csv("/home/vishwesh/Documents/aggregated_transaction.csv")
        agg_txn.columns = agg_txn.columns.str.strip().str.lower().str.replace(" ", "_")
        st.success("✅ Transaction data loaded successfully!")
        st.write("📄 Transaction Columns:", agg_txn.columns.tolist())
    except Exception as e:
        st.error(f"❌ Could not load Transaction CSV: {e}")
        st.stop()

    expected_txn_cols = {'state', 'year', 'quarter', 'transaction_type', 'count', 'amount'}
    missing = expected_txn_cols - set(agg_txn.columns)
    if missing:
        st.error(f"❌ Missing columns in aggregated.csv: {missing}")
        st.stop()

    agg_txn['amount'] = pd.to_numeric(agg_txn['amount'], errors='coerce')
    agg_txn['count'] = pd.to_numeric(agg_txn['count'], errors='coerce')
    agg_txn = agg_txn.dropna(subset=['state', 'year', 'quarter', 'transaction_type'])

    state = st.selectbox("Select State", sorted(agg_txn['state'].unique()))
    year = st.selectbox("Select Year", sorted(agg_txn['year'].unique()))
    quarter = st.selectbox("Select Quarter", sorted(agg_txn['quarter'].unique()))

    filtered_txn = agg_txn[
        (agg_txn['state'] == state) &
        (agg_txn['year'] == year) &
        (agg_txn['quarter'] == quarter)
    ]

    st.subheader(f"🧾 Transactions in {state} - Q{quarter} {year}")
    st.dataframe(filtered_txn)

    fig_amount = px.bar(
        filtered_txn,
        x='transaction_type',
        y='amount',
        color='transaction_type',
        title="💰 Transaction Amount by Type",
        labels={'amount': 'Amount (INR)', 'transaction_type': 'Type'}
    )
    st.plotly_chart(fig_amount)

    fig_count = px.bar(
        filtered_txn,
        x='transaction_type',
        y='count',
        color='transaction_type',
        title="🔢 Transaction Count by Type",
        labels={'count': 'Count', 'transaction_type': 'Type'}
    )
    st.plotly_chart(fig_count)

# ------------------ DEVICE BRAND DASHBOARD ------------------

elif page == "Device Brand Usage":
    st.title("📱 Device Brand Usage Analysis")

    try:
        brand_df = pd.read_csv("/home/vishwesh/Documents/aggregated_user1.csv")
        brand_df.columns = brand_df.columns.str.strip().str.lower().str.replace(" ", "_")
        brand_df.rename(columns={'brand': 'device_brand'}, inplace=True)
        st.success("✅ Device brand data loaded successfully!")
        st.write("📄 Brand Data Columns:", brand_df.columns.tolist())
    except Exception as e:
        st.error(f"❌ Could not load Device Brand CSV: {e}")
        st.stop()

    required_cols = {'state', 'year', 'quarter', 'device_brand'}
    missing = required_cols - set(brand_df.columns)
    if missing:
        st.error(f"❌ Missing columns in device_brand_usage.csv: {missing}")
        st.stop()

    brand_df = brand_df.dropna(subset=list(required_cols))
    brand_df['count'] = pd.to_numeric(brand_df['count'], errors='coerce')
    brand_df['percentage'] = pd.to_numeric(brand_df['percentage'], errors='coerce')

    state = st.selectbox("Select State", sorted(brand_df['state'].unique()))
    year = st.selectbox("Select Year", sorted(brand_df['year'].unique()))
    quarter = st.selectbox("Select Quarter", sorted(brand_df['quarter'].unique()))

    filtered_brand = brand_df[
        (brand_df['state'] == state) &
        (brand_df['year'] == year) &
        (brand_df['quarter'] == quarter)
    ]

    st.subheader(f"📊 Device Usage in {state} - Q{quarter} {year}")
    st.dataframe(filtered_brand)

    fig_device_count = px.bar(
        filtered_brand.sort_values(by='count', ascending=False),
        x='device_brand',
        y='count',
        color='device_brand',
        title="🔢 User Count by Device Brand",
        labels={'count': 'Users'}
    )
    st.plotly_chart(fig_device_count)

    fig_device_percent = px.bar(
        filtered_brand.sort_values(by='percentage', ascending=False),
        x='device_brand',
        y='percentage',
        color='device_brand',
        title="📈 Usage Share (%) by Device Brand",
        labels={'percentage': 'Usage %'}
    )
    st.plotly_chart(fig_device_percent)


# ------------------ INSURANCE DASHBOARD ------------------

elif page == "Insurance Analysis (State-level)":
    st.title("🛡️ Insurance Analysis - State Level")

    try:
        # Load the insurance dataset
        ins_df = pd.read_csv("/home/vishwesh/Documents/aggregated_insurance.csv")
        ins_df.columns = ins_df.columns.str.strip().str.lower().str.replace(" ", "_")
        st.success("✅ Insurance state-level data loaded!")
        st.write("📄 Insurance Data Columns:", ins_df.columns.tolist())
    except Exception as e:
        st.error(f"❌ Could not load insurance CSV: {e}")
        st.stop()

    # Required columns check
    required_cols = {'state', 'year', 'quarter', 'count', 'amount'}
    missing = required_cols - set(ins_df.columns)
    if missing:
        st.error(f"❌ Missing columns in insurance data: {missing}")
        st.stop()

    # Data cleaning and conversion
    ins_df = ins_df.dropna(subset=list(required_cols))
    ins_df['count'] = pd.to_numeric(ins_df['count'], errors='coerce')
    ins_df['amount'] = pd.to_numeric(ins_df['amount'], errors='coerce')

    # Dropdown filters
    state = st.selectbox("Select State", sorted(ins_df['state'].unique()))
    year = st.selectbox("Select Year", sorted(ins_df['year'].unique()))

    filtered_ins = ins_df[
        (ins_df['state'] == state) &
        (ins_df['year'] == year)
    ].sort_values(by='quarter')

    if filtered_ins.empty:
        st.warning("⚠️ No insurance data available for this filter.")
    else:
        st.subheader(f"📊 Insurance Data for {state} - {year}")
        st.dataframe(filtered_ins)

        # Quarter vs Amount
        fig_amt = px.line(
            filtered_ins,
            x='quarter',
            y='amount',
            markers=True,
            title="💰 Insurance Amount per Quarter",
            labels={'amount': 'Amount (INR)', 'quarter': 'Quarter'}
        )
        st.plotly_chart(fig_amt)

        # Quarter vs Count
        fig_cnt = px.line(
            filtered_ins,
            x='quarter',
            y='count',
            markers=True,
            title="🔢 Insurance Count per Quarter",
            labels={'count': 'Policies', 'quarter': 'Quarter'}
        )
        st.plotly_chart(fig_cnt)



# ------------------ USER ENGAGEMENT ANALYSIS ------------------

elif page == "User Engagement (District-level)":
    st.title("📍 User Engagement - District Level")

    try:
        # Load user engagement district-level data
        user_df = pd.read_csv("/home/vishwesh/Documents/maps_user.csv")
        user_df.columns = user_df.columns.str.strip().str.lower().str.replace(" ", "_")
        st.success("✅ User engagement data loaded successfully!")
        st.write("📄 Columns:", user_df.columns.tolist())
    except Exception as e:
        st.error(f"❌ Could not load user engagement CSV: {e}")
        st.stop()

    # Required columns check
    required_cols = {'state', 'year', 'quarter', 'district', 'registeredusers', 'appopens'}
    missing = required_cols - set(user_df.columns)
    if missing:
        st.error(f"❌ Missing required columns: {missing}")
        st.stop()

    # Clean & convert columns
    user_df = user_df.dropna(subset=list(required_cols))
    user_df['registeredusers'] = pd.to_numeric(user_df['registeredusers'], errors='coerce')
    user_df['appopens'] = pd.to_numeric(user_df['appopens'], errors='coerce')

    # Dropdown filters
    state = st.selectbox("Select State", sorted(user_df['state'].unique()))
    year = st.selectbox("Select Year", sorted(user_df['year'].unique()))

    filtered_user = user_df[
        (user_df['state'] == state) &
        (user_df['year'] == year)
    ].sort_values(by='quarter')

    if filtered_user.empty:
        st.warning("⚠️ No user engagement data found for the selected filters.")
    else:
        st.subheader(f"📊 User Engagement in {state} - {year}")
        st.dataframe(filtered_user)

        # Line chart - Registered Users
        fig_registered = px.line(
            filtered_user,
            x='quarter',
            y='registeredusers',
            color='district',
            markers=True,
            title="👥 Registered Users per District (Quarter-wise)",
            labels={'registeredusers': 'Registered Users'}
        )
        st.plotly_chart(fig_registered)

        # Line chart - App Opens
        fig_appopens = px.line(
            filtered_user,
            x='quarter',
            y='appopens',
            color='district',
            markers=True,
            title="📱 App Opens per District (Quarter-wise)",
            labels={'appopens': 'App Opens'}
        )
        st.plotly_chart(fig_appopens)




#----------Transaction Analysis (District-Level)----------------------

elif page == "Transaction Analysis (District-level)":
    st.title("📍 Transaction Analysis - District Level")

    try:
        # Load district-level transaction data
        txn_dist_df = pd.read_csv("/home/vishwesh/Documents/maps_transaction.csv")
        txn_dist_df.columns = txn_dist_df.columns.str.strip().str.lower().str.replace(" ", "_")
        st.success("✅ District-level transaction data loaded!")
        st.write("📄 Columns:", txn_dist_df.columns.tolist())
    except Exception as e:
        st.error(f"❌ Could not load maps_transaction.csv: {e}")
        st.stop()

    # Required columns check
    required_cols = {'state', 'year', 'quarter', 'district', 'count', 'amount'}
    missing = required_cols - set(txn_dist_df.columns)
    if missing:
        st.error(f"❌ Missing required columns in transaction data: {missing}")
        st.stop()

    # Clean & convert
    txn_dist_df = txn_dist_df.dropna(subset=list(required_cols))
    txn_dist_df['count'] = pd.to_numeric(txn_dist_df['count'], errors='coerce')
    txn_dist_df['amount'] = pd.to_numeric(txn_dist_df['amount'], errors='coerce')

    # Dropdown filters
    state = st.selectbox("Select State", sorted(txn_dist_df['state'].unique()))
    year = st.selectbox("Select Year", sorted(txn_dist_df['year'].unique()))

    filtered_txn_dist = txn_dist_df[
        (txn_dist_df['state'] == state) &
        (txn_dist_df['year'] == year)
    ].sort_values(by='quarter')

    if filtered_txn_dist.empty:
        st.warning("⚠️ No transaction data available for the selected filters.")
    else:
        st.subheader(f"📊 Transactions in {state} - {year}")
        st.dataframe(filtered_txn_dist)

        # Line Chart - Transaction Amount by District
        fig_amount = px.line(
            filtered_txn_dist,
            x='quarter',
            y='amount',
            color='district',
            markers=True,
            title="💰 Transaction Amount per District (Quarter-wise)",
            labels={'amount': 'Amount (INR)', 'quarter': 'Quarter'}
        )
        st.plotly_chart(fig_amount)

        # Line Chart - Transaction Count by District
        fig_count = px.line(
            filtered_txn_dist,
            x='quarter',
            y='count',
            color='district',
            markers=True,
            title="🔢 Transaction Count per District (Quarter-wise)",
            labels={'count': 'Transactions', 'quarter': 'Quarter'}
        )
        st.plotly_chart(fig_count)

#-----------Insurance District level Analysis--------------------
elif page == "Insurance Analysis (District-level)":
    st.title("🏥 Insurance Analysis - District Level")

    try:
        # Load district-level insurance data
        ins_dist_df = pd.read_csv("/home/vishwesh/Documents/maps_insurance-dir1.csv")
        ins_dist_df.columns = ins_dist_df.columns.str.strip().str.lower().str.replace(" ", "_")
        st.success("✅ District-level insurance data loaded successfully!")
        st.write("📄 Columns:", ins_dist_df.columns.tolist())
    except Exception as e:
        st.error(f"❌ Could not load insurance district CSV: {e}")
        st.stop()

    # Required columns check
    required_cols = {'state', 'year', 'quarter', 'district', 'count', 'amount'}
    missing = required_cols - set(ins_dist_df.columns)
    if missing:
        st.error(f"❌ Missing required columns: {missing}")
        st.stop()

    # Data cleanup
    ins_dist_df = ins_dist_df.dropna(subset=list(required_cols))
    ins_dist_df['count'] = pd.to_numeric(ins_dist_df['count'], errors='coerce')
    ins_dist_df['amount'] = pd.to_numeric(ins_dist_df['amount'], errors='coerce')

    # Dropdown filters
    state = st.selectbox("Select State", sorted(ins_dist_df['state'].unique()))
    year = st.selectbox("Select Year", sorted(ins_dist_df['year'].unique()))

    filtered_ins_dist = ins_dist_df[
        (ins_dist_df['state'] == state) &
        (ins_dist_df['year'] == year)
    ].sort_values(by='quarter')

    if filtered_ins_dist.empty:
        st.warning("⚠️ No district-level insurance data found for this filter.")
    else:
        st.subheader(f"📊 Insurance in {state} - {year}")
        st.dataframe(filtered_ins_dist)

        # Line Chart - Transaction Amount
        fig_amt = px.line(
            filtered_ins_dist,
            x='quarter',
            y='amount',
            color='district',
            markers=True,
            title="💰 Insurance Amount per District (Quarter-wise)",
            labels={'amount': 'Amount (INR)', 'quarter': 'Quarter'}
        )
        st.plotly_chart(fig_amt)

        # Line Chart - Transaction Count
        fig_cnt = px.line(
            filtered_ins_dist,
            x='quarter',
            y='count',
            color='district',
            markers=True,
            title="🔢 Insurance Count per District (Quarter-wise)",
            labels={'count': 'Transactions', 'quarter': 'Quarter'}
        )
        st.plotly_chart(fig_cnt)









