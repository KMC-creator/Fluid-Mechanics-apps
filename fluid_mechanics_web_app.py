import math
import streamlit as st

# Constants
g = 9.81  # Acceleration due to gravity (m/s^2)

# Functions for calculations
def calculate_pressure_drop(L, D, V, f):
    """
    Calculate the pressure drop (head loss) given pipe length, diameter, velocity, and friction factor.
    """
    h_f = f * (L / D) * (V**2 / (2 * g))
    return h_f

def calculate_flow_rate(L, D, h_f, f):
    """
    Calculate the flow rate (velocity) given pipe length, diameter, head loss, and friction factor.
    """
    V = math.sqrt((2 * g * h_f * D) / (f * L))
    return V

def calculate_pipe_diameter(L, V, h_f, f):
    """
    Calculate the pipe diameter given pipe length, velocity, head loss, and friction factor.
    """
    D = (f * L * V**2) / (2 * g * h_f)
    return D

# Streamlit App
def main():
    st.title("Fluid Mechanics Calculator")
    st.write("Select the type of problem to solve:")

    # Problem type selection
    problem_type = st.radio(
        "Problem Type",
        options=[
            "1. Determine pressure drop (head loss)",
            "2. Determine flow rate (velocity)",
            "3. Determine pipe diameter",
        ],
    )

    # Input fields
    L = st.number_input("Pipe Length (m)", min_value=0.0, value=100.0)
    D = st.number_input("Pipe Diameter (m)", min_value=0.0, value=0.1)
    V = st.number_input("Flow Velocity (m/s)", min_value=0.0, value=2.0)
    h_f = st.number_input("Head Loss (m)", min_value=0.0, value=5.0)
    f = st.number_input("Friction Factor", min_value=0.0, value=0.02)

    # Calculate button
    if st.button("Calculate"):
        try:
            if problem_type == "1. Determine pressure drop (head loss)":
                h_f = calculate_pressure_drop(L, D, V, f)
                st.success(f"Pressure Drop (Head Loss): {h_f:.4f} m")
            elif problem_type == "2. Determine flow rate (velocity)":
                V = calculate_flow_rate(L, D, h_f, f)
                st.success(f"Flow Velocity: {V:.4f} m/s")
            elif problem_type == "3. Determine pipe diameter":
                D = calculate_pipe_diameter(L, V, h_f, f)
                st.success(f"Pipe Diameter: {D:.4f} m")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Run the app
if __name__ == "__main__":
    main()