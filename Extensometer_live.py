import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
import os

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if not st.session_state.password_correct:
        with st.form("password_form"):
            st.markdown("""
                <div style='padding:2rem; background-color:#f5f5f5; border-radius:10px;'>
                    <h3>🔐 Access Restricted!</h3>
                    <p>Please enter the password to continue.</p>
                </div>
            """, unsafe_allow_html=True)

            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Submit")

            if submitted:
                if password == "LetMeIn123":
                    st.session_state.password_correct = True
                else:
                    st.error("Access denied. Please try again.")
                    st.stop()

    if not st.session_state.password_correct:
        st.stop()

# ⛔️ STOP EVERYTHING if password isn't correct


def main_app():
    # Auto-refresh every 10 minutes (600000 milliseconds)
    st_autorefresh(interval=600000, key="csv_autorefresh")
    
    # Public Google Drive CSV link
    CSV_URL = "https://drive.google.com/uc?export=download&id=1pJmaYBl8j-sfIqXFEU4V8riKDUomYTtO"
    
    
    # Hard-coded constant row
    constants_row = {
        'Date': '09/01/2025',
        'Time': '05:00',
        'Temperature (°C)': 27,
        'Battery Voltage (V)': 13.2711,
        'Signal 1': 0.073,
        'Signal 2': 0.0349,
        'Signal 3': 0.1787,
        'Ext1 - O-p / 5 V i-p': 0.0146,
        'Ext1 - Using calibn No. 1 (mm)': 0.027181591,
        'Ext1 - Move from rdgs start 1-1': 0,
        'Ext1 - Using calibn No. 2 (mm)': -0.14321684,
        'Ext1 - Move from rdgs start 1-2': 0,
        'Ext1 - Using calibn No. 3 (mm)': -0.273843431,
        'Ext1 - Move from rdgs start 1-3': 0,
        'Ext1 - Mean of 3 calibn (mm)': 0,
        'Ext1 - Microstrain on 700mm': 0,
        'Ext2 - O-p / 5 V i-p': 0.00698,
        'Ext2 - Using calibn No. 1 (mm)': -0.009454694,
        'Ext2 - Move from rdgs start 2-1': 0,
        'Ext2 - Using calibn No. 2 (mm)': -0.220929668,
        'Ext2 - Move from rdgs start 2-2': 0,
        'Ext2 - Using calibn No. 3 (mm)': -0.370621559,
        'Ext2 - Move from rdgs start 2-3': 0,
        'Ext2 - Mean of 3 calibn (mm)': 0,
        'Ext2 - Microstrain on 700mm': 0,
        'Ext3 - O-p / 5 V i-p': 0.03574,
        'Ext3 - Using calibn No. 1 (mm)': 0.125411409,
        'Ext3 - Move from rdgs start 3-1': 0,
        'Ext3 - Using calibn No. 2 (mm)': 0.028515776,
        'Ext3 - Move from rdgs start 3-2': 0,
        'Ext3 - Using calibn No. 3 (mm)': -0.067679789,
        'Ext3 - Move from rdgs start 3-3': 0,
        'Ext3 - Mean of 3 calibn (mm)': 0,
        'Ext3 - Microstrain on 700mm': 0
    }
    
    try:
            
            df = pd.read_csv(CSV_URL, header=None)
            df[['Date', 'Time']] = df[0].str.strip().str.split(' ', n=1, expand=True)
            df['Date'] = pd.to_datetime(df['Date'], format='%y/%m/%d').dt.strftime('%d/%m/%Y')
            df = df.drop(columns=[0])
            df.columns = ['Value 1', 'Value 2', 'Value 3', 'Value 4', 'Value 5', 'Date', 'Time']
            df = df[['Date', 'Time', 'Value 1', 'Value 2', 'Value 3', 'Value 4', 'Value 5']]
            df.columns = ['Date', 'Time', 'Temperature (°C)', 'Battery Voltage (V)', 'Signal 1', 'Signal 2', 'Signal 3']
    
            # Add extensometer columns
            ext_columns = []
            for i in range(1, 4):
                ext_columns.extend([
                    f"Ext{i} - O-p / 5 V i-p",
                    f"Ext{i} - Using calibn No. 1 (mm)",
                    f"Ext{i} - Move from rdgs start {i}-1",
                    f"Ext{i} - Using calibn No. 2 (mm)",
                    f"Ext{i} - Move from rdgs start {i}-2",
                    f"Ext{i} - Using calibn No. 3 (mm)",
                    f"Ext{i} - Move from rdgs start {i}-3",
                    f"Ext{i} - Mean of 3 calibn (mm)",
                    f"Ext{i} - Microstrain on 700mm"
                ])
            for col in ext_columns:
                df[col] = None
    
            constants_df = pd.DataFrame([constants_row])[df.columns]
            full_df = pd.concat([constants_df, df], ignore_index=True)
    
            # --- CALCULATIONS ---
    
            # Shared coefficients
            def apply_poly(x, coefs):
                return sum(c * x**p for p, c in enumerate(reversed(coefs)))
    
            # Polynomial coefficients
            poly_1 = [632.1661, -456.938, 141.769, -12.6897, 5.03271, -0.0440119]
            poly_2 = [1764.0067, -1719.5542, 651.97883, -105.53222, 12.248305, -0.30149893]
            poly_3 = [2224.8258, -2238.1605, 870.29635, -147.20228, 15.573023, -0.47244019]
    
            for i in range(1, 4):
                s_col = f"Signal {i}"
                op_col = f"Ext{i} - O-p / 5 V i-p"
                full_df.loc[1:, op_col] = full_df.loc[1:, s_col] / 5
    
                x = full_df.loc[1:, op_col]
                full_df.loc[1:, f"Ext{i} - Using calibn No. 1 (mm)"] = apply_poly(x, poly_1)
                full_df.loc[1:, f"Ext{i} - Move from rdgs start {i}-1"] = (
                    full_df.loc[1:, f"Ext{i} - Using calibn No. 1 (mm)"] - full_df.loc[0, f"Ext{i} - Using calibn No. 1 (mm)"]
                )
    
                full_df.loc[1:, f"Ext{i} - Using calibn No. 2 (mm)"] = apply_poly(x, poly_2)
                full_df.loc[1:, f"Ext{i} - Move from rdgs start {i}-2"] = (
                    full_df.loc[1:, f"Ext{i} - Using calibn No. 2 (mm)"] - full_df.loc[0, f"Ext{i} - Using calibn No. 2 (mm)"]
                )
    
                full_df.loc[1:, f"Ext{i} - Using calibn No. 3 (mm)"] = apply_poly(x, poly_3)
                full_df.loc[1:, f"Ext{i} - Move from rdgs start {i}-3"] = (
                    full_df.loc[1:, f"Ext{i} - Using calibn No. 3 (mm)"] - full_df.loc[0, f"Ext{i} - Using calibn No. 3 (mm)"]
                )
    
                full_df.loc[1:, f"Ext{i} - Mean of 3 calibn (mm)"] = (
                    full_df.loc[1:, f"Ext{i} - Move from rdgs start {i}-1"] +
                    full_df.loc[1:, f"Ext{i} - Move from rdgs start {i}-2"] +
                    full_df.loc[1:, f"Ext{i} - Move from rdgs start {i}-3"]
                ) / 3
    
                full_df.loc[1:, f"Ext{i} - Microstrain on 700mm"] = (
                    full_df.loc[1:, f"Ext{i} - Mean of 3 calibn (mm)"] / 700 * 1_000_000
                )
    
            st.success("File processed and all calculations complete.")
            
            # Extract last row values
            last_row = full_df.iloc[-1]
            last_time = f"{last_row['Date']} at {last_row['Time']}"
            e1 = round(last_row['Ext1 - Microstrain on 700mm'], 2)
            e2 = round(last_row['Ext2 - Microstrain on 700mm'], 2)
            e3 = round(last_row['Ext3 - Microstrain on 700mm'], 2)
                 
                    
            # Display "last reading" banner from the most recent row
            with st.container():
                st.markdown(
                    f"""
                    <div style="
                        background-color: #fff9c4;
                        padding: 1rem;
                        border-radius: 0.5rem;
                        border: 1px solid #f0e68c;
                        box-shadow: 1px 1px 5px rgba(0,0,0,0.05);
                        ">
                        <h4>📡 Last Reading Received</h4>
                        <b>Date & Time:</b> {last_row['Date']} at {last_row['Time']}<br>
                        <b>Extensometer 1 Microstrain:</b> {e1}<br>
                        <b>Extensometer 2 Microstrain:</b> {e2}<br>
                        <b>Extensometer 3 Microstrain:</b> {e3}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Get max compressive and tensile strains recorded to date
            microstrain_cols = [
                "Ext1 - Microstrain on 700mm",
                "Ext2 - Microstrain on 700mm",
                "Ext3 - Microstrain on 700mm"
            ]
    
            max_compressive = full_df[microstrain_cols].min().min()  # Most negative
            max_tensile = full_df[microstrain_cols].max().max()      # Most positive
    
            # Locate timestamps of max strain values
            max_comp_loc = full_df[microstrain_cols].stack().idxmin()
            max_tens_loc = full_df[microstrain_cols].stack().idxmax()
    
            # Extract date, time, and extensometer
            comp_row = full_df.loc[max_comp_loc[0]]
            tens_row = full_df.loc[max_tens_loc[0]]
    
            comp_timestamp = f"{comp_row['Date']} at {comp_row['Time']} (from {max_comp_loc[1].split()[0]})"
            tens_timestamp = f"{tens_row['Date']} at {tens_row['Time']} (from {max_tens_loc[1].split()[0]})"
                 
    
            # Create combined datetime column
            full_df["Datetime"] = pd.to_datetime(full_df["Date"] + " " + full_df["Time"], format="%d/%m/%Y %H:%M", errors="coerce")
    
            # Melt the DataFrame to long format for plotting
            melted = pd.melt(
                full_df,
                id_vars=["Datetime"],
                value_vars=[
                    "Ext1 - Microstrain on 700mm",
                    "Ext2 - Microstrain on 700mm",
                    "Ext3 - Microstrain on 700mm"
                ],
                var_name="Extensometer",
                value_name="Microstrain"
            )
    
            # Filter out the constants row (NaNs or zeros)
            melted = melted.dropna(subset=["Datetime", "Microstrain"])
    
            
            st.markdown("### 📊 Microstrain Charts")
            # Plot interactive scatter chart
            fig = px.scatter(
                melted,
                x="Datetime",
                y="Microstrain",
                color="Extensometer",
                title="Microstrain on 700mm vs. Time",
                labels={"Microstrain": "Microstrain (με)", "Datetime": "Timestamp"},
                hover_data={"Microstrain": True, "Datetime": True}
            )
            fig.update_traces(mode="markers")
    
            st.plotly_chart(fig, use_container_width=True)
            
            # Temperature over time (line chart)
            st.markdown("### 🌡️ Temperature Over Time")
            fig_temp = px.line(
                full_df[1:],  # skip constants row
                x="Datetime",
                y="Temperature (°C)",
                title="Temperature Over Time",
                labels={"Temperature (°C)": "Temperature (°C)", "Datetime": "Timestamp"},
            )
    
            # Update styling: no markers, yellow line
            fig_temp.update_traces(mode="lines", line=dict(color="orange"))
    
            st.plotly_chart(fig_temp, use_container_width=True)
    
            st.markdown("### 🚨 Maximum Compression and Tensile Strains Recorded To Date")
            # Compression Gauge
            gauge_compression = go.Figure(go.Indicator(
                mode="gauge+number",
                value=abs(max_compressive),
                title={
                        "text": f"Max Compressive Strain (με)<br><sub>{comp_timestamp}</sub>",
                        "font": {"size": 20}
                        },
                gauge={
                    "axis": {"range": [0, 5000]},
                    "bar": {"color": "blue"},
                    "steps": [
                        {"range": [0, 2000], "color": "lightgreen"},
                        {"range": [2000, 3500], "color": "orange"},
                        {"range": [3500, 5000], "color": "red"}
                    ],
                    "threshold": {
                        "line": {"color": "red", "width": 4},
                        "thickness": 0.75,
                        "value": 3500
                    }
                }
            ))
    
            # Tension Gauge
            gauge_tension = go.Figure(go.Indicator(
                mode="gauge+number",
                value=max_tensile,
                 title={
                    "text": f"Max Tensile Strain (με)<br><sub>{tens_timestamp}</sub>",
                    "font": {"size": 20}
                    },
                gauge={
                    "axis": {"range": [0, 200]},
                    "bar": {"color": "blue"},
                    "steps": [
                        {"range": [0, 50], "color": "lightgreen"},
                        {"range": [50, 100], "color": "orange"},
                        {"range": [100, 200], "color": "red"}
                    ],
                    "threshold": {
                        "line": {"color": "red", "width": 4},
                        "thickness": 0.75,
                        "value": 100
                    }
                }
            ))
            col1, col2 = st.columns(2)
            col1.plotly_chart(gauge_compression, use_container_width=True)
            col2.plotly_chart(gauge_tension, use_container_width=True)
            
            # Show the full DataFrame
            st.markdown("### 📋 Raw Data & Calculations")
            st.dataframe(full_df)
            st.markdown(
                """
                <marquee behavior="scroll" direction="left" scrollamount="5"
                        style="color: white; background-color: #333;
                                padding: 10px; font-weight: bold; font-size: 16px;
                                border-radius: 10px; margin-top: 30px;">
                    📡 CREDITS 📡 Back-End and Data Transmission : Dennis Louw | Post-Processing and Dashboard : Grant Harli (J&W) | Extensometer Hardware and Installation : Dr Irvin Luker |   🚀
                </marquee>
                """,
                unsafe_allow_html=True
            )

    except Exception as e:
        st.error(f"Error loading CSV from Google Drive: {e}")
        st.stop()

check_password()

st.set_page_config(
    page_title="Extensometer Dashboard – Holftontein Site",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
    <div style='text-align: center; padding: 2rem 0; background-color: #003366; color: white; border-radius: 10px;'>
        <h1 style='margin-bottom: 0;'>📡 Extensometer Dashboard</h1>
        <h3 style='margin-top: 0;'>Holftontein Site – Real-Time Structural Monitoring</h3>
    </div>
""", unsafe_allow_html=True)


main_app()  # 👈 only runs if password was correct

