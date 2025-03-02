import pandas as pd
import streamlit as st

def load_lease_data(file_path):
    """Loads the Porsche lease residual data."""
    return pd.read_excel(file_path)

def get_base_residual(df, year, model):
    """Retrieve base residual value for given inputs."""
    try:
        # Ensure lease term is fixed at 39 months
        df = df[df["Lease Term (Months)"] == 39]
        
        # Debugging output
        st.write("Available Years:", df["Model Year"].unique().tolist())
        st.write("Available Models:", df["Model"].unique().tolist())
        
        # Filtering data
        model_data = df[df["Model"] == model]
        year_data = model_data[model_data["Model Year"] == year]
        
        if year_data.empty:
            return "Error: Residual not found"
        
        return year_data["Base Residual (%)"].values[0]
    except Exception as e:
        return f"Error: {str(e)}"

def adjust_residual_for_miles(miles):
    """Adjust residual based on mileage brackets."""
    if miles <= 18000:
        return 0
    elif 18001 <= miles <= 24000:
        return -1
    elif 24001 <= miles <= 30000:
        return -2
    else:
        return -3  # Ensure it always returns a numeric value

def calculate_residual(file_path, year, model, mileage):
    """Calculates the final residual value based on user input."""
    df = load_lease_data(file_path)
    base_residual = get_base_residual(df, year, model)
    mileage_adjustment = adjust_residual_for_miles(mileage)
    
    st.write(f"Debug: Base Residual = {base_residual}, Mileage Adjustment = {mileage_adjustment}")
    
    if isinstance(base_residual, (int, float)) and isinstance(mileage_adjustment, (int, float)):
        total_residual = base_residual + mileage_adjustment
    else:
        total_residual = "Error: Could not calculate total residual"
    
    return base_residual, mileage_adjustment, total_residual

def main():
    st.title("Porsche Lease Calculator")
    file_path = "Porsche_Lease_Calculator.xlsx"
    
    df = load_lease_data(file_path)
    available_models = df["Model"].unique().tolist()
    
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
