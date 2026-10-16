import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp


# 1. Define the derivative of B(r)
# NOTE: This is a placeholder function.
# You must replace this with the actual derivative of your function B(r).
# For this example, let's assume B(r) = 1/r, so dB/dr = -1/r^2.
def B_prime(r):
    """
    Returns the value of dB/dr at a given radius r.
    """
    # --- REPLACE THIS WITH YOUR FUNCTION ---
    return -1.0 / r**2
    # ------------------------------------


# 2. Define the system of first-order ODEs
def ode_system(r, y, B_prime_func):
    """
    Defines the system dy/dr for the ODE solver.
    y is a vector [Sigma, dSigma/dr].
    """
    Sigma, dSigma_dr = y

    # Equation for the second derivative from the original ODE
    d2Sigma_dr2 = -Sigma * (B_prime_func(r)) ** 2 / 4.0

    return [dSigma_dr, d2Sigma_dr2]


# 3. Set up integration parameters
r_max = 100.0  # A sufficiently "large" starting radius
r_min = 0.1  # The minimum radius to solve down to

# 4. Set the boundary ("initial") conditions at r_max
# From Sigma(r) ≈ r and dSigma/dr(r) ≈ 1 for large r
Sigma_at_rmax = r_max
dSigma_dr_at_rmax = 1.0
y_initial = [Sigma_at_rmax, dSigma_dr_at_rmax]

# 5. Define the integration range (from r_max down to r_min)
r_span = [r_max, r_min]

# Define the points where you want the solution
r_eval = np.linspace(r_max, r_min, 500)

# 6. Solve the ODE system
solution = solve_ivp(
    fun=lambda r, y: ode_system(r, y, B_prime),  # The ODE system function
    t_span=r_span,  # Integration interval
    y0=y_initial,  # Initial conditions at r_max
    t_eval=r_eval,  # Points to evaluate the solution at
    method="RK45",  # Standard Runge-Kutta solver
)

# 7. Extract and plot the results
# The results need to be sorted because we integrated backward
sort_indices = np.argsort(solution.t)
r_plot = solution.t[sort_indices]
Sigma_plot = solution.y[0][sort_indices]

print(f"Calculation successful. Found {len(r_plot)} solution points.")

# Plotting
plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(r_plot, Sigma_plot, label=r"Numerical Solution for $\Sigma(r)$", color="blue", linewidth=2)
ax.plot(r_plot, r_plot, label="Asymptotic Behavior ($y=r$)", color="red", linestyle="--", dashes=(5, 5))

ax.set_xlabel("$r$", fontsize=14)
ax.set_ylabel(r"$\Sigma(r)$", fontsize=14)
ax.set_title("Numerical Solution of the ODE", fontsize=16)
ax.legend(fontsize=12)
ax.set_xlim(left=0)
ax.set_ylim(bottom=0)

plt.show()
