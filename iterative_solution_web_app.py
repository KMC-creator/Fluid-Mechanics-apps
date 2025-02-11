import math
import streamlit as st

# Constants
g = 9.81  # Acceleration due to gravity (m/s^2)

# Colebrook equation to calculate friction factor (f)
def colebrook(Re, epsilon_D):
    """
    Solve the Colebrook equation iteratively to find the friction factor (f).
    Re: Reynolds number
    epsilon_D: Relative roughness (epsilon / D)
    """
    # Initial guess for f (common starting point)
    f = 0.02
    tolerance = 1e-6  # Convergence tolerance
    max_iterations = 1000  # Maximum iterations to avoid infinite loops

    for i in range(max_iterations):
        # Colebrook equation
        new_f = (-2 * math.log10((epsilon_D / 3.7) + (2.51 / (Re * math.sqrt(f))))) ** -2

        # Check for convergence
        if abs(new_f - f) < tolerance:
            return new_f

        # Update f for the next iteration
        f = new_f

    # If no convergence, return the last value
    return f

# Function to calculate Reynolds number
def reynolds_number(V, D, nu):
    """
    Calculate Reynolds number.
    V: Flow velocity (m/s)
    D: Pipe diameter (m)
    nu: Kinematic viscosity (m^2/s)
    """
    return (V * D) / nu

# Function to calculate flow velocity (V)
def calculate_flow_rate(L, D, h_f, epsilon_D, nu):
    """
    Calculate flow velocity (V) iteratively using the Colebrook equation.
    L: Pipe length (m)
    D: Pipe diameter (m)
    h_f: Head loss (m)
    epsilon_D: Relative roughness (epsilon / D)
    nu: Kinematic viscosity (m^2/s)
    """
    # Initial guess for V
    V = 1.0  # Initial guess (m/s)
    tolerance = 1e-6  # Convergence tolerance
    max_iterations = 1000  # Maximum iterations

    for i in range(max_iterations):
        # Calculate Reynolds number
        Re = reynolds_number(V, D, nu)

        # Calculate friction factor using Colebrook equation
        f = colebrook(Re, epsilon_D)

        # Calculate new velocity using Darcy-Weisbach equation
        new_V = math.sqrt((2 * g * h_f * D) / (f * L))

        # Check for convergence
        if abs(new_V - V) < tolerance:
            return new_V

        # Update V for the next iteration
        V = new_V

    # If no convergence, return the last value
    return V

# Streamlit App
def main():
    st.title("Fluid Mechanics Iterative Solution")
    st.write("This app calculates flow velocity and flow rate using the Colebrook equation.")

    # Input fields
    L = st.number_input("Pipe Length (m)", min_value=0.0, value=100.0)  # Pipe length
    D = st.number_input("Pipe Diameter (m)", min_value=0.0, value=0.1)  # Pipe diameter
    h_f = st.number_input("Head Loss (m)", min_value=0.0, value=5.0)  # Head loss
    epsilon_D = st.number_input("Relative Roughness (epsilon / D)", min_value=0.0, value=0.001)  # Relative roughness
    nu = st.number_input("Kinematic Viscosity (m^2/s)", min_value=0.0, value=1e-6)  # Kinematic viscosity

    # Calculate button
    if st.button("Calculate"):
        try:
            # Calculate flow velocity (V)
            V = calculate_flow_rate(L, D, h_f, epsilon_D, nu)

            # Calculate flow rate (Q)
            A = (math.pi / 4) * D**2  # Cross-sectional area of the pipe
            Q = V * A  # Flow rate (m^3/s)

            # Display results
            st.success(f"Flow Velocity (V): {V:.4f} m/s")
            st.success(f"Flow Rate (Q): {Q:.6f} m^3/s")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Run the app
if __name__ == "__main__":
    main()