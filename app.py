import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Data Preparation (previous data remains the same)
inflation_data = pd.DataFrame({
    "Year": [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "Inflation": [0.20, -0.06, 0.18, 1.43, 1.74, 1.63, 0.48, 2.55, 8.83, 6.30, 2.40]
})

sp500_data = pd.DataFrame({
    "Year": [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "Return": [13.69, 1.38, 11.96, 21.83, -4.38, 31.49, 18.40, 28.71, -18.11, 26.29, 25.02]
})

european_index_data = pd.DataFrame({
    "Year": [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "Return": [4.35, 6.79, -1.20, 7.68, -13.24, 23.16, -4.04, 22.25, -12.90, 12.74, 6.0]
})

real_estate_data = pd.DataFrame({
    "Year": [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "Return": [3.2, 4.1, 5.6, 5.3, 4.7, 5.0, 3.8, 7.1, 6.0, 4.5, 2.3]
})

gold_data = pd.DataFrame({
    "Year": [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "Return": [-0.19, -11.59, 8.63, 12.57, -1.15, 18.83, 24.43, -3.51, -0.23, 13.08, 27.23]
})

crypto_data = pd.DataFrame({
    "Year": [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "Return": [-58.6, 35.4, 125.8, 1331.0, -72.6, 87.2, 302.8, 59.8, -64.2, 155.9, 121.1]
})

bank_data = pd.DataFrame({
    "Year": [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "Return": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Hypothetical bank interest rates
})

# Sidebar for Investment Parameters
st.sidebar.header("Investment Parameters")
initial_investment = st.sidebar.number_input("Initial Investment (€):", min_value=100, value=10000, step=100)
start_year = st.sidebar.selectbox("Starting Year", options=list(range(2014, 2025)))
inflation_adjustment = st.sidebar.checkbox("Adjust for Inflation", value=True)

# Asset Selection
st.sidebar.header("Asset Selection")
selected_assets = st.sidebar.multiselect(
    "Choose Assets to Display", 
    options=["S&P 500", "STOXX Europe 600", "EU Real Estate", "Gold", "Crypto", "Bank Account"],
    default=["S&P 500", "STOXX Europe 600", "EU Real Estate", "Gold", "Bank Account"]
)

# Filter datasets for selected start year and assets
datasets = {
    "S&P 500": sp500_data,
    "STOXX Europe 600": european_index_data,
    "EU Real Estate": real_estate_data,
    "Gold": gold_data,
    "Crypto": crypto_data,
    "Bank Account": bank_data
}

filtered_datasets = {
    name: df[df["Year"] >= start_year].reset_index(drop=True) 
    for name, df in datasets.items() 
    if name in selected_assets
}

# Calculate investment growth
def calculate_growth(df, initial_amount, inflation_data, adjust_for_inflation=True):
    values = [initial_amount]
    
    for i, ret in enumerate(df["Return"]):
        # Get corresponding inflation rate
        year = df["Year"].iloc[i]
        
        # Find inflation rate, use last known rate if not found
        inflation_row = inflation_data[inflation_data["Year"] == year]
        if len(inflation_row) > 0:
            inflation_rate = inflation_row["Inflation"].values[0] / 100
        else:
            # Use the most recent available inflation rate
            inflation_rate = inflation_data["Inflation"].iloc[-1] / 100
        
        # Adjust return for inflation if selected
        if adjust_for_inflation:
            # Use real return calculation
            real_return = (1 + ret/100) / (1 + inflation_rate) - 1
            next_value = values[-1] * (1 + real_return)
        else:
            # Simple nominal return calculation
            next_value = values[-1] * (1 + ret/100)
        
        values.append(next_value)
    
    return values[1:]  # Return values excluding the initial investment


# Combine all data into a single DataFrame for plotting
growth_data = pd.DataFrame({"Year": filtered_datasets[list(filtered_datasets.keys())[0]]["Year"]})
for name, df in filtered_datasets.items():
    growth_data[name] = calculate_growth(df, initial_investment, inflation_data, inflation_adjustment)

# Plot combined growth chart
plt.figure(figsize=(12, 8))
for col in growth_data.columns[1:]:
    plt.plot(growth_data["Year"], growth_data[col], label=col)

plt.title("Investment Growth" + (" (Inflation-Adjusted)" if inflation_adjustment else ""), fontsize=16)
plt.xlabel("Year", fontsize=14)
plt.ylabel("Portfolio Value (€)", fontsize=14)
plt.legend(title="Asset Class")
plt.grid(True)
st.pyplot(plt)

# Show raw data
if st.checkbox("Show Raw Data"):
    st.write(growth_data)

st.sidebar.markdown("""
---
### Notes
- **S&P 500** and **STOXX Europe 600** returns are **without dividends** (price returns only).
- **Real Estate** values are **without rental income** (capital appreciation only).
""")