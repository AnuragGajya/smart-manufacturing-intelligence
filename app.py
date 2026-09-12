# ============================================================
# SMART MANUFACTURING INTELLIGENCE
# REAL-TIME PREDICTIVE MAINTENANCE DASHBOARD
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pickle
from datetime import datetime
import time
from pathlib import Path

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart Manufacturing Intelligence",
    page_icon="🏭",
    layout="wide"
)

# ============================================================
# AUTO REFRESH
# ============================================================

from streamlit_autorefresh import st_autorefresh

st_autorefresh(
    interval=3000,
    key="refresh"
)

# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "best_model.pkl"
SCALER_PATH = BASE_DIR / "data_scaler.pkl"

# ============================================================
# LOAD MODEL AND SCALER
# ============================================================

@st.cache_resource
def load_model():

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    with open(SCALER_PATH, "rb") as f:
        scaler = pickle.load(f)

    return model, scaler


try:

    model, scaler = load_model()

    model_loaded = True

except Exception as e:

    model_loaded = False

    st.error("❌ Could not load the model or scaler.")

    st.code(str(e))

    st.info(
        "Make sure best_model.pkl and data_scaler.pkl "
        "are in the same folder as app.py."
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div style="
        background:linear-gradient(90deg,#0A1628,#1D7A5F);
        padding:20px;
        border-radius:10px;
        color:white;
        text-align:center;
        margin-bottom:20px;
    ">

        <h1>🏭 Smart Manufacturing Intelligence</h1>

        <p>Real-Time Predictive Maintenance Dashboard</p>

    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    f"Last updated: {datetime.now().strftime('%H:%M:%S')}"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ Control Panel")

st.sidebar.markdown(
    """
    ### Dashboard Features

    🔴 High Risk Detection

    🟡 Medium Risk Detection

    🟢 Low Risk Detection

    📊 Real-Time Analytics

    🔧 Manual Prediction

    💰 Financial Impact
    """
)

st.sidebar.divider()

st.sidebar.subheader("🔧 Manual Machine Prediction")


# ============================================================
# MANUAL INPUTS
# ============================================================

machine_type = st.sidebar.selectbox(
    "Machine Type",
    ["H", "L", "M"]
)

air_t = st.sidebar.slider(
    "Air Temperature [K]",
    min_value=295.0,
    max_value=305.0,
    value=300.0
)

proc_t = st.sidebar.slider(
    "Process Temperature [K]",
    min_value=305.0,
    max_value=315.0,
    value=310.0
)

rpm = st.sidebar.slider(
    "Rotational Speed [rpm]",
    min_value=1000.0,
    max_value=3000.0,
    value=1500.0
)

torque = st.sidebar.slider(
    "Torque [Nm]",
    min_value=3.0,
    max_value=80.0,
    value=40.0
)

wear = st.sidebar.slider(
    "Tool Wear [min]",
    min_value=0.0,
    max_value=250.0,
    value=100.0
)

predict_button = st.sidebar.button(
    "🔮 Predict Machine Risk",
    use_container_width=True
)


# ============================================================
# LIVE DATA GENERATION
# ============================================================

def get_live_data():

    np.random.seed(
        int(time.time()) % 1000
    )

    n = 10

    return pd.DataFrame({

        "Machine_ID":
            [f"M-{i:03d}" for i in range(1, n + 1)],

        "Type":
            np.random.choice(
                ["H", "L", "M"],
                n
            ),

        "Air temperature [K]":
            np.random.uniform(
                295,
                305,
                n
            ),

        "Process temperature [K]":
            np.random.uniform(
                305,
                315,
                n
            ),

        "Rotational speed [rpm]":
            np.random.uniform(
                1000,
                3000,
                n
            ),

        "Torque [Nm]":
            np.random.uniform(
                3,
                80,
                n
            ),

        "Tool wear [min]":
            np.random.uniform(
                0,
                250,
                n
            )
    })


# ============================================================
# MAIN DASHBOARD
# ============================================================

if model_loaded:

    # ========================================================
    # GET LIVE DATA
    # ========================================================

    df = get_live_data()


    # ========================================================
    # TYPE ENCODING
    # ========================================================

    type_mapping = {
        "H": 0,
        "L": 1,
        "M": 2
    }

    df["Type_encoded"] = (
        df["Type"].map(type_mapping)
    )


    # ========================================================
    # FEATURE ENGINEERING
    # ========================================================

    df["temp_diff"] = (
        df["Process temperature [K]"]
        -
        df["Air temperature [K]"]
    )

    df["power"] = (
        df["Rotational speed [rpm]"]
        *
        df["Torque [Nm]"]
    )

    df["tool_wear_rate"] = (
        df["Tool wear [min]"]
        /
        (
            df["Rotational speed [rpm]"]
            + 1
        )
    )


    # ========================================================
    # MODEL FEATURES
    # ========================================================

    features = [

        "Air temperature [K]",

        "Process temperature [K]",

        "Rotational speed [rpm]",

        "Torque [Nm]",

        "Tool wear [min]",

        "temp_diff",

        "power",

        "tool_wear_rate",

        "Type_encoded"

    ]


    # ========================================================
    # SCALE DATA
    # ========================================================

    X_scaled = scaler.transform(
        df[features]
    )


    # ========================================================
    # PREDICT FAILURE PROBABILITY
    # ========================================================

    df["Failure_Probability"] = (
        model.predict_proba(
            X_scaled
        )[:, 1]
    )


    # ========================================================
    # RISK CLASSIFICATION
    # ========================================================

    df["Risk_Level"] = pd.cut(

        df["Failure_Probability"],

        bins=[
            0,
            0.3,
            0.7,
            1.0
        ],

        labels=[
            "Low",
            "Medium",
            "High"
        ],

        include_lowest=True
    )


    # ========================================================
    # SEPARATE RISK GROUPS
    # ========================================================

    high = df[
        df["Risk_Level"] == "High"
    ]

    medium = df[
        df["Risk_Level"] == "Medium"
    ]

    low = df[
        df["Risk_Level"] == "Low"
    ]


    # ========================================================
    # FACTORY OVERVIEW
    # ========================================================

    st.subheader(
        "📊 Factory Overview"
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "🔧 Total Machines",
        len(df)
    )

    c2.metric(
        "🔴 High Risk",
        len(high)
    )

    c3.metric(
        "🟡 Medium Risk",
        len(medium)
    )

    c4.metric(
        "🟢 Low Risk",
        len(low)
    )

    c5.metric(
        "⚡ System Status",
        "LIVE"
    )


    st.divider()


    # ========================================================
    # MANUAL MACHINE PREDICTION
    # ========================================================

    if predict_button:

        # ----------------------------------------------------
        # FEATURE ENGINEERING
        # ----------------------------------------------------

        temp_diff = (
            proc_t - air_t
        )

        power = (
            rpm * torque
        )

        tool_wear_rate = (
            wear / (rpm + 1)
        )


        # ----------------------------------------------------
        # TYPE ENCODING
        # ----------------------------------------------------

        type_encoded = type_mapping[
            machine_type
        ]


        # ----------------------------------------------------
        # CREATE INPUT DATAFRAME
        # ----------------------------------------------------

        manual_input = pd.DataFrame([{

            "Air temperature [K]":
                air_t,

            "Process temperature [K]":
                proc_t,

            "Rotational speed [rpm]":
                rpm,

            "Torque [Nm]":
                torque,

            "Tool wear [min]":
                wear,

            "temp_diff":
                temp_diff,

            "power":
                power,

            "tool_wear_rate":
                tool_wear_rate,

            "Type_encoded":
                type_encoded

        }])


        # ----------------------------------------------------
        # SCALE MANUAL INPUT
        # ----------------------------------------------------

        manual_scaled = scaler.transform(
            manual_input[features]
        )


        # ----------------------------------------------------
        # PREDICT
        # ----------------------------------------------------

        probability = (
            model.predict_proba(
                manual_scaled
            )[0, 1]
        )


        # ----------------------------------------------------
        # RISK LEVEL
        # ----------------------------------------------------

        if probability < 0.3:

            risk = "LOW"

        elif probability < 0.7:

            risk = "MEDIUM"

        else:

            risk = "HIGH"


        # ----------------------------------------------------
        # DISPLAY RESULT
        # ----------------------------------------------------

        st.subheader(
            "🔮 Manual Machine Prediction"
        )

        m1, m2, m3 = st.columns(3)

        m1.metric(
            "Machine Type",
            machine_type
        )

        m2.metric(
            "Failure Probability",
            f"{probability:.2%}"
        )

        m3.metric(
            "Risk Level",
            risk
        )


        # ----------------------------------------------------
        # GAUGE
        # ----------------------------------------------------

        gauge = go.Figure(

            go.Indicator(

                mode="gauge+number",

                value=probability * 100,

                title={
                    "text":
                    "Failure Probability (%)"
                },

                gauge={

                    "axis": {
                        "range": [
                            0,
                            100
                        ]
                    },

                    "steps": [

                        {
                            "range": [
                                0,
                                30
                            ]
                        },

                        {
                            "range": [
                                30,
                                70
                            ]
                        },

                        {
                            "range": [
                                70,
                                100
                            ]
                        }

                    ],

                    "threshold": {

                        "line": {
                            "width": 4
                        },

                        "value":
                            probability * 100

                    }

                }

            )

        )

        gauge.update_layout(
            height=350
        )

        st.plotly_chart(
            gauge,
            use_container_width=True
        )


    # ========================================================
    # TABS
    # ========================================================

    tab1, tab2, tab3 = st.tabs([

        "📊 Live Dashboard",

        "🔧 Machine Status",

        "💰 Financial Impact"

    ])


    # ========================================================
    # TAB 1 — LIVE DASHBOARD
    # ========================================================

    with tab1:

        st.subheader(
            "📈 Real-Time Machine Analytics"
        )


        col1, col2 = st.columns(2)


        # ----------------------------------------------------
        # TEMPERATURE CHART
        # ----------------------------------------------------

        with col1:

            temp_df = pd.DataFrame({

                "Machine":
                    df["Machine_ID"],

                "Air Temperature":
                    df[
                        "Air temperature [K]"
                    ],

                "Process Temperature":
                    df[
                        "Process temperature [K]"
                    ]

            })


            fig_temp = go.Figure()


            fig_temp.add_trace(

                go.Scatter(

                    x=temp_df["Machine"],

                    y=temp_df[
                        "Air Temperature"
                    ],

                    mode="lines+markers",

                    name="Air Temperature"

                )

            )


            fig_temp.add_trace(

                go.Scatter(

                    x=temp_df["Machine"],

                    y=temp_df[
                        "Process Temperature"
                    ],

                    mode="lines+markers",

                    name="Process Temperature"

                )

            )


            fig_temp.update_layout(

                title=
                "🌡️ Temperature by Machine",

                xaxis_title=
                "Machine",

                yaxis_title=
                "Temperature [K]"

            )


            st.plotly_chart(

                fig_temp,

                use_container_width=True

            )


        # ----------------------------------------------------
        # TOOL WEAR VS FAILURE RISK
        # ----------------------------------------------------

        with col2:

            fig_scatter = px.scatter(

                df,

                x="Tool wear [min]",

                y="Failure_Probability",

                size="Torque [Nm]",

                hover_name="Machine_ID",

                hover_data=[
                    "Type",
                    "Rotational speed [rpm]"
                ],

                title=
                "🔧 Tool Wear vs Failure Probability"

            )


            fig_scatter.update_layout(

                xaxis_title=
                "Tool Wear [min]",

                yaxis_title=
                "Failure Probability"

            )


            st.plotly_chart(

                fig_scatter,

                use_container_width=True

            )


        # ----------------------------------------------------
        # RISK DISTRIBUTION + AVERAGE RISK
        # ----------------------------------------------------

        col3, col4 = st.columns(2)


        # ----------------------------------------------------
        # RISK PIE CHART
        # ----------------------------------------------------

        with col3:

            risk_counts = (
                df["Risk_Level"]
                .value_counts()
            )


            fig_pie = px.pie(

                values=
                risk_counts.values,

                names=
                risk_counts.index,

                title=
                "🚦 Risk Distribution"

            )


            st.plotly_chart(

                fig_pie,

                use_container_width=True

            )


        # ----------------------------------------------------
        # AVERAGE FACTORY RISK
        # ----------------------------------------------------

        with col4:

            average_risk = (

                df[
                    "Failure_Probability"
                ].mean()

                * 100

            )


            avg_gauge = go.Figure(

                go.Indicator(

                    mode="gauge+number",

                    value=average_risk,

                    title={
                        "text":
                        "Average Factory Risk (%)"
                    },

                    gauge={

                        "axis": {
                            "range": [
                                0,
                                100
                            ]
                        },

                        "steps": [

                            {
                                "range": [
                                    0,
                                    30
                                ]
                            },

                            {
                                "range": [
                                    30,
                                    70
                                ]
                            },

                            {
                                "range": [
                                    70,
                                    100
                                ]
                            }

                        ]

                    }

                )

            )


            avg_gauge.update_layout(
                height=350
            )


            st.plotly_chart(

                avg_gauge,

                use_container_width=True

            )


    # ========================================================
    # TAB 2 — MACHINE STATUS
    # ========================================================

    with tab2:

        st.subheader(
            "🔧 Current Machine Status"
        )


        display_df = df[

            [

                "Machine_ID",

                "Type",

                "Risk_Level",

                "Failure_Probability",

                "Tool wear [min]",

                "Torque [Nm]",

                "Rotational speed [rpm]"

            ]

        ].copy()


        display_df[
            "Failure_Probability"
        ] = (

            display_df[
                "Failure_Probability"
            ]

            .apply(
                lambda x:
                f"{x:.2%}"
            )

        )


        # ----------------------------------------------------
        # ACTION
        # ----------------------------------------------------

        display_df["Action"] = np.where(

            df["Risk_Level"] == "High",

            "🚨 Immediate Maintenance",

            np.where(

                df["Risk_Level"] == "Medium",

                "⚠️ Schedule Inspection",

                "✅ Normal Operation"

            )

        )


        # ----------------------------------------------------
        # RENAME COLUMNS
        # ----------------------------------------------------

        display_df.rename(

            columns={

                "Machine_ID":
                    "Machine",

                "Type":
                    "Type",

                "Risk_Level":
                    "Risk",

                "Failure_Probability":
                    "Failure Probability",

                "Tool wear [min]":
                    "Tool Wear",

                "Torque [Nm]":
                    "Torque",

                "Rotational speed [rpm]":
                    "RPM"

            },

            inplace=True

        )


        st.dataframe(

            display_df,

            use_container_width=True,

            hide_index=True

        )


        # ----------------------------------------------------
        # ACTIVE ALERTS
        # ----------------------------------------------------

        st.subheader(
            "🚨 Active Alerts"
        )


        if len(high) > 0:

            for _, row in high.iterrows():

                st.error(

                    f"🚨 {row['Machine_ID']} "
                    f"is HIGH RISK — "
                    f"Failure probability: "
                    f"{row['Failure_Probability']:.2%}"

                )

        else:

            st.success(
                "✅ No high-risk machines detected."
            )


    # ========================================================
    # TAB 3 — FINANCIAL IMPACT
    # ========================================================

    with tab3:

        st.subheader(
            "💰 Predictive Maintenance Financial Impact"
        )


        col1, col2 = st.columns(2)


        # ----------------------------------------------------
        # INPUTS
        # ----------------------------------------------------

        with col1:

            cost_failure = st.number_input(

                "Cost per Machine Failure ($)",

                min_value=0.0,

                value=5000.0,

                step=500.0

            )


            false_alarm_cost = st.number_input(

                "Cost per False Alarm ($)",

                min_value=0.0,

                value=200.0,

                step=50.0

            )


        with col2:

            total_machines = st.number_input(

                "Total Machines",

                min_value=1,

                value=100

            )


            working_days = st.number_input(

                "Working Days per Year",

                min_value=1,

                value=300

            )


        # ----------------------------------------------------
        # ASSUMPTIONS
        # ----------------------------------------------------

        annual_failure_rate = 0.034

        detection_rate = 0.96

        missed_rate = 0.04

        false_alarm_rate = 0.05


        # ----------------------------------------------------
        # CALCULATIONS
        # ----------------------------------------------------

        expected_failures = (

            total_machines

            *

            annual_failure_rate

            *

            working_days

            /

            30

        )


        failures_prevented = (

            expected_failures

            *

            detection_rate

        )


        failures_missed = (

            expected_failures

            *

            missed_rate

        )


        false_alarms = (

            expected_failures

            *

            false_alarm_rate

        )


        savings = (

            failures_prevented

            *

            cost_failure

        )


        false_alarm_cost_total = (

            false_alarms

            *

            false_alarm_cost

        )


        net_savings = (

            savings

            -

            false_alarm_cost_total

        )


        # ----------------------------------------------------
        # FINANCIAL METRICS
        # ----------------------------------------------------

        f1, f2, f3, f4 = st.columns(4)


        f1.metric(

            "Expected Failures",

            f"{expected_failures:.1f}"

        )


        f2.metric(

            "Failures Prevented",

            f"{failures_prevented:.1f}"

        )


        f3.metric(

            "Estimated Savings",

            f"${savings:,.0f}"

        )


        f4.metric(

            "Net Savings",

            f"${net_savings:,.0f}"

        )


        st.divider()


        # ----------------------------------------------------
        # FINANCIAL CHART
        # ----------------------------------------------------

        financial_data = pd.DataFrame({

            "Category": [

                "Failure Cost Avoided",

                "False Alarm Cost",

                "Net Savings"

            ],

            "Amount": [

                savings,

                false_alarm_cost_total,

                net_savings

            ]

        })


        fig_financial = px.bar(

            financial_data,

            x="Category",

            y="Amount",

            title=
            "💵 Estimated Financial Impact"

        )


        fig_financial.update_layout(

            yaxis_title=
            "Amount ($)",

            xaxis_title=""

        )


        st.plotly_chart(

            fig_financial,

            use_container_width=True

        )


        st.info(

            "ℹ️ Financial calculations are project "
            "assumptions for demonstration. Replace "
            "these values with your company's actual "
            "failure rate, maintenance cost and false "
            "alarm cost for real ROI analysis."

        )


# ============================================================
# MODEL LOADING ERROR
# ============================================================

else:

    st.warning(

        "Dashboard cannot start because the model "
        "or scaler could not be loaded."

    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(

    "Smart Manufacturing Intelligence | "
    "Anurag Gajya | Electronics Data Analyst"

)