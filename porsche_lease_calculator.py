import pandas as pd
import streamlit as st

def load_lease_data(file_path):
    """Loads the Porsche lease residual data."""
    return pd.read_excel(file_path, sheet_name=None)  # Load all sheets

def get_base_residual(df, year, model):
    """Retrieve base residual value for given inputs."""
    try:
        lease_df = df['Lease Lookup']  # Ensure we reference the correct sheet
        lease_df = lease_df[lease_df["Lease Term (Months)"] == 39]
        
        # Debugging output
        st.write("Available Years:", lease_df["Model Year"].unique().tolist())
        st.write("Available Models:", lease_df["Model"].unique().tolist())
        
        # Filtering data
        model_data = lease_df[lease_df["Model"] == model]
        year_data = model_data[model_data["Model Year"] == year]
        
        if year_data.empty:
            st.write("Error: No matching data found for the selected model and year.")
            return None  # Return None instead of a string error
        
        residual_value = year_data["Base Residual (%)"].values[0]
        return float(residual_value)  # Ensure it's a numeric value
    except Exception as e:
        st.write(f"Error retrieving base residual: {str(e)}")
        return None

def adjust_residual_for_miles(df, year, miles):
    """Adjust residual based on mileage brackets from the 'Miles' sheet."""
    try:
        miles_df = df['Miles']  # Ensure we reference the correct sheet
        year_data = miles_df[miles_df["Year"] == year]
        
        if year_data.empty:
            st.write("Error: No mileage data found for this year.")
            return 0  # Default to no adjustment
        
        # Find the correct mileage adjustment
        adjustment_row = year_data[(year_data["B"] <= miles) & (year_data["C"] >= miles)]
        
        if adjustment_row.empty:
            return 0  # Default to no adjustment if mileage is out of range
        
        return float(adjustment_row["D"].values[0])
    except Exception as e:
        st.write(f"Error retrieving mileage adjustment: {str(e)}")
        return 0

def calculate_residual(file_path, year, model, mileage):
    """Calculates the final residual value based on user input."""
    df = load_lease_data(file_path)
    base_residual = get_base_residual(df, year, model)
    mileage_adjustment = adjust_residual_for_miles(df, year, mileage)
    
    st.write(f"Debug: Base Residual = {base_residual}, Mileage Adjustment = {mileage_adjustment}")
    
    if base_residual is not None and isinstance(mileage_adjustment, (int, float)):
        total_residual = base_residual + mileage_adjustment
    else:
        total_residual = "Error: Could not calculate total residual"
    
    return base_residual, mileage_adjustment, total_residual

def main():
    st.title("Porsche Lease Calculator")
    file_path = "Porsche_Lease_Calculator.xlsx"
    
    df = load_lease_data(file_path)
    available_models = df['Lease Lookup']["Model"].unique().tolist()
    
    vehicle_year = st.number_input("Enter Vehicle Year", min_value=2000, max_value=2025, step=1)
    vehicle_model = st.selectbox("Select Model", available_models)
    mileage = st.number_input("Enter Mileage", min_value=0, step=1)
    
    if st.button("Calculate Residual"):
        base_residual, mileage_adjustment, total_residual = calculate_residual(file_path, vehicle_year, vehicle_model, mileage)
        
        st.write(f"**Base Residual:** {base_residual}%")
        st.write(f"**Mileage Adjustment:** {mileage_adjustment}%")
        st.write(f"**Total Residual:** {total_residual}%")

if __name__ == "__main__":
    main()
