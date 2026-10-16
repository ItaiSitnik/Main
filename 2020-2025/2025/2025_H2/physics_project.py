# main_solver_isotropic.py

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_bvp, solve_ivp


class HomogeneousIsotropizationEvolver:
    """
    Implements the time-evolution for the spatially homogeneous isotropization
    problem from Sec. 4.1 of Chesler & Yaffe (arXiv:1309.1439).

    This version is fully self-contained and produces a non-trivial evolution.
    """

    def __init__(self, u_grid):
        """
        Initializes the solver using the inverted radial coordinate u = 1/r.

        Args:
            u_grid (np.array): The radial grid for the simulation, from u=0 to u_h.
        """
        self.u = u_grid
        self.u_boundary = u_grid[0]  # Should be 0
        self.u_horizon = u_grid[-1]  # Inner boundary (horizon)

        # Evolved field is B(u). a4 is a constant of motion here.
        self.B = np.zeros_like(self.u)
        self.a4 = 0.0

        # Storage for results
        self.history = {"t": [], "pressure_anisotropy": []}

    def set_initial_conditions(self, a4_0, B_0_func):
        """
        Sets the initial conditions for a4 and B(u) at t=0.
        """
        self.a4 = a4_0
        self.B = B_0_func(self.u)
        print(f"Initial conditions set: a4={self.a4:.4f}")
        self._store_history_and_anisotropy(0.0)

    # --- ODE Solvers based on Sec. 4.1 of Chesler & Yaffe ---

    def _solve_for_sigma(self):
        """Solves eq. 4.2a for Sigma."""
        duB = np.gradient(self.B, self.u)

        def ode_sigma(u, y):
            # y = [Sigma, Sigma']
            duB_interp = np.interp(u, self.u, duB)
            d2Sigma = -0.5 * y[0] * (duB_interp**2)
            return np.vstack((y[1], d2Sigma))

        def bc_sigma(ya, yb):
            # BC at u=0 (ya): Sigma ~ 1/u => (u*Sigma)' = 0
            # A numerically stable condition is u*Sigma' + Sigma = 0 at u=epsilon
            # BC at u_horizon (yb): We don't have a strict condition, so we
            # can leave it free and rely on the u=0 condition.
            # Let's use the asymptotic form: Sigma(u_b) = 1/u_b
            # Sigma'(u_b) = -1/u_b^2
            # Here ya is at u_boundary=0, yb is at u_horizon.
            # Numerically, u=0 is singular, so we evaluate at the first grid point u[1]
            return np.array([self.u[1] * ya[1] + ya[0], yb[0] - 1.0 / self.u_horizon])

        y_guess = np.zeros((2, self.u.size))
        y_guess[0] = 1.0 / self.u
        y_guess[0, 0] = 1e9  # Avoid division by zero

        res = solve_bvp(ode_sigma, bc_sigma, self.u, y_guess, tol=1e-4)
        if not res.success:
            raise RuntimeError(f"Solver for Sigma failed: {res.message}")
        return res.sol(self.u)[0]

    def _solve_for_sigma_dot(self, Sigma):
        """Solves eq. 4.2c for Sigma_dot."""
        duSigma = np.gradient(Sigma, self.u)

        def ode_sigma_dot(u, y):
            Sigma_interp = np.interp(u, self.u, Sigma)
            duSigma_interp = np.interp(u, self.u, duSigma)
            return -2 * (duSigma_interp / Sigma_interp) * y + 2 * u**-2 * Sigma_interp

        # Solve as IVP from u=0 (boundary) inwards to u_horizon
        y0 = [-self.a4]  # Asymptotic behavior from T_00
        sol = solve_ivp(ode_sigma_dot, [self.u[1], self.u_horizon], y0, t_eval=self.u[1:], dense_output=True)

        full_sol = np.concatenate(([y0[0]], sol.y[0]))
        return full_sol

    def _solve_for_B_dot(self, Sigma, Sigma_dot):
        """Solves eq. 4.3 for B_dot."""
        duSigma = np.gradient(Sigma, self.u)
        duB = np.gradient(self.B, self.u)

        def ode_B_dot(u, y):
            Sigma_interp = np.interp(u, self.u, Sigma)
            duSigma_interp = np.interp(u, self.u, duSigma)
            duB_interp = np.interp(u, self.u, duB)
            Sigma_dot_interp = np.interp(u, self.u, Sigma_dot)
            return -1.5 * (duSigma_interp / Sigma_interp) * y - 1.5 * (duB_interp * Sigma_dot_interp) / (
                Sigma_interp * u**-2
            )

        y0 = [0.0]  # B_dot vanishes at the boundary
        sol = solve_ivp(ode_B_dot, [self.u[1], self.u_horizon], y0, t_eval=self.u[1:], dense_output=True)
        full_sol = np.concatenate(([y0[0]], sol.y[0]))
        return full_sol

    def _solve_for_A(self, Sigma, Sigma_dot, B_dot):
        """Solves eq. 4.2b for A."""
        duSigma = np.gradient(Sigma, self.u)
        duB = np.gradient(self.B, self.u)

        def ode_A(u, y):
            Sigma_interp = np.interp(u, self.u, Sigma)
            duSigma_interp = np.interp(u, self.u, duSigma)
            Sigma_dot_interp = np.interp(u, self.u, Sigma_dot)
            duB_interp = np.interp(u, self.u, duB)
            B_dot_interp = np.interp(u, self.u, B_dot)

            d2A = (
                -6 * (duSigma_interp / Sigma_interp) * Sigma_dot_interp * u**-2
                + 1.5 * duB_interp * B_dot_interp
                + 2 * u**-2
            )
            return np.vstack((y[1], d2A))

        def bc_A(ya, yb):
            # BC at u=0 (ya): A ~ 0.5/u^2 => (u^2*A)' -> 0
            # BC at u_horizon (yb): Horizon stationarity condition A_h = -1/4 (d+B)^2
            # Here B_dot is d+B. So A(u_h) = -0.25 * B_dot(u_h)^2
            B_dot_h = B_dot[-1]
            return np.array([2 * self.u[1] * ya[0] + self.u[1] ** 2 * ya[1], yb[0] + 0.25 * B_dot_h**2])

        y_guess = np.zeros((2, self.u.size))
        y_guess[0] = 0.5 / self.u**2
        y_guess[0, 0] = 1e9

        res = solve_bvp(ode_A, bc_A, self.u, y_guess, tol=1e-4)
        if not res.success:
            raise RuntimeError(f"Solver for A failed: {res.message}")
        return res.sol(self.u)[0]

    def _store_history_and_anisotropy(self, t):
        self.history["t"].append(t)
        # Pressure anisotropy is proportional to b4 = lim u->0 (B/u^4)
        # We can approximate this from the first few grid points
        # From B ~ b4*u^4, we get B/u^3 ~ b4*u, so derivative is b4
        b4 = np.gradient(self.B / self.u**3, self.u)[1] if self.u[1] > 0 else 0
        self.history["pressure_anisotropy"].append(b4)

    def step(self, dt):
        """Performs one full time step of the evolution."""
        Sigma = self._solve_for_sigma()
        Sigma_dot = self._solve_for_sigma_dot(Sigma)
        B_dot = self._solve_for_B_dot(Sigma, Sigma_dot)
        A = self._solve_for_A(Sigma, Sigma_dot, B_dot)

        duB = np.gradient(self.B, self.u)
        dtB = B_dot - A * duB

        # Evolve B using Forward Euler
        self.B += dtB * dt

    def evolve(self, t_final, dt):
        """Runs the simulation from t=0 to t_final."""
        current_t = 0.0
        num_steps = int(t_final / dt)

        for i in range(num_steps):
            try:
                self.step(dt)
                current_t += dt
                self._store_history_and_anisotropy(current_t)
                if (i + 1) % 5 == 0:
                    print(f"Time: {current_t:.2f}, Anisotropy Coeff: {self.history['pressure_anisotropy'][-1]:.4f}")
            except RuntimeError as e:
                print(f"Evolution failed at t={current_t:.2f}. Error: {e}")
                break
        print("Evolution finished.")

    def plot_results(self):
        """Plots the time evolution of the pressure anisotropy."""
        plt.style.use("seaborn-v0_8-whitegrid")
        fig, ax = plt.subplots(figsize=(10, 6))

        t = np.array(self.history["t"])
        anisotropy = np.array(self.history["pressure_anisotropy"])

        ax.plot(t, anisotropy, "b-o", markersize=4, label="Pressure Anisotropy $\propto b^{(4)}(t)$")
        ax.set_xlabel("Time $t$")
        ax.set_ylabel("Pressure Anisotropy $\delta p / p_{eq}$")
        ax.set_title("Homogeneous Isotropization (Chesler & Yaffe, sec. 4.1)")
        ax.legend()
        plt.show()


if __name__ == "__main__":
    # --- Simulation Setup using u=1/r grid ---
    # Boundary at u=0, Horizon at u=1
    u_horizon = 1.0
    N_u = 50
    # We use a grid that is denser near u=0 (Chebyshev-like)
    u_grid = u_horizon * (1 - np.cos(np.linspace(0, np.pi / 2, N_u)))

    # --- Initial Conditions from Chesler & Yaffe eq 4.7 ---
    # Use their parameters to get a result similar to their Fig. 3
    beta_param = 5.0
    u0_param = 0.25
    w_param = 0.15
    alpha_param = 1.0

    a4_initial = -0.5 * alpha_param

    def B_initial_func(u):
        # Redefined b = u^-3 B from eq. 4.7
        b = beta_param * u * np.exp(-((u - u0_param) ** 2) / w_param**2)
        # We need B = u^3 * b
        return u**3 * b

    # --- Run the Simulation ---
    evolver = HomogeneousIsotropizationEvolver(u_grid=u_grid)
    evolver.set_initial_conditions(a4_0=a4_initial, B_0_func=B_initial_func)

    evolver.evolve(t_final=4.0, dt=0.02)

    evolver.plot_results()
