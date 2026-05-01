import streamlit as st
import pandas as pd

from main import run_pipeline

st.set_page_config(page_title="Airline Fuel Optimization", layout="wide")


# HEADER

st.title(" Airline Fuel Optimization Agent")
st.markdown("Optimize fuel usage using AI + Weather + Aircraft Performance")


mode = st.radio("Select Input Mode:", [" Sample Flights", " Custom Flight"])

flights = []


if mode == " Sample Flights":

    df = pd.read_csv("data/flights.csv")

    st.subheader(" Flight Data")
    st.dataframe(df, use_container_width=True)

    flights = df.to_dict(orient="records")



elif mode == " Custom Flight":

    st.subheader("Enter Flight Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        flight_id = st.text_input("Flight ID", "AI999")
        origin = st.text_input("Origin", "DEL")
        destination = st.text_input("Destination", "DXB")

    with col2:
        route = st.text_input("Route", "DEL-KAR-DXB")
        altitude = st.slider("Altitude (ft)", 30000, 40000, 35000)

    with col3:
        aircraft = st.selectbox("Aircraft", ["A320", "B737"])

    flights = [{
        "flight_id": flight_id,
        "origin": origin,
        "destination": destination,
        "route": route,
        "altitude": altitude,
        "aircraft": aircraft
    }]



st.markdown("---")

if st.button(" Run Optimization"):

    with st.spinner("Running AI Optimization..."):

        results = run_pipeline(flights)

    st.success(" Optimization Completed")

    
    # RESULTS TABLE
   
    st.subheader(" Optimization Results")

    table_data = []
    for r in results:
        table_data.append({
            "Flight": r["flight_id"],
            "Route": f"{r['origin']} → {r['destination']}",
            "Fuel Before (kg)": r["original_fuel"],
            "Fuel After (kg)": r["optimized_fuel"],
            "Savings (kg)": r["savings_kg"],
            "Savings (%)": r["savings_pct"],
            "Recommended Action": r["recommended_action"]
        })

    result_df = pd.DataFrame(table_data)

    st.dataframe(result_df, use_container_width=True)

    
    # SUMMARY METRICS
    
    st.subheader(" Summary")

    total_savings = sum(r["savings_kg"] for r in results)
    avg_savings = sum(r["savings_pct"] for r in results) / len(results)

    col1, col2 = st.columns(2)

    col1.metric("Total Fuel Saved (kg)", round(total_savings, 2))
    col2.metric("Average Savings (%)", round(avg_savings, 2))

    
    st.subheader("AI Flight Recommendations")

    for r in results:
        st.info(f" {r['flight_id']}: {r['rationale']}")
