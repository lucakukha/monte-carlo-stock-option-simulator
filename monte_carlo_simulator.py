import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Page setup
st.set_page_config(page_title="Monte Carlo Stock Simulator", page_icon="📈", layout="centered")

# Track which page we are on
if "page" not in st.session_state:
    st.session_state.page = "home"


def go(page):
    st.session_state.page = page


# Basic styling
st.markdown(
    """
    <style>
    body { background-color: #e6f0ff; }
    .stButton>button {
        background-color: #1f77b4; 
        color: white; 
        border-radius: 10px;
        height: 3em; 
        width: 16em; 
        font-size: 16px; 
        font-weight: 600;
    }
    .stButton>button:hover { 
        background-color: #145a8d; 
        color: #e6f0ff; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Home
if st.session_state.page == "home":
    st.title("🎯 Monte Carlo Stock Simulator")
    st.markdown(
        "Explore stock price behaviour using Geometric Brownian Motion (GBM) "
        "and Monte Carlo simulation."
    )

    # Center the buttons
    col_left, col_mid, col_right = st.columns([1, 1, 1])
    with col_mid:
        if st.button("📈 Simulate Stock Paths"):
            go("simulate")

        st.markdown("")  # spacing

        if st.button("📘 Theory / Help"):
            st.info(
                "Coming soon. I plan to add a brief explanation of GBM, Monte Carlo, "
                "and the Black–Scholes model."
            )

    st.markdown("---")
    st.caption("© 2025 Luca Kukhaleishvili | GBM Monte Carlo project (work in progress)")

# Simulate Page
elif st.session_state.page == "simulate":
    st.title("📈 Simulate Stock Paths")
    st.markdown(
        "Enter parameters below. Defaults are chosen to be roughly realistic for a large index "
        "such as the S&P 500."
    )

    # Input form
    with st.form("params"):
        stock = st.text_input(
            "Stock / Label",
            value="S&P 500 (demo)",
            help="Used in chart titles and captions.",
        )
        S0 = st.number_input(
            "S₀ — Start Price",
            min_value=0.01,
            value=1000.0,
            step=10.0,
            help="Initial price at time t = 0.",
        )
        mu = st.number_input(
            "μ — Annual Drift (Expected Return)",
            value=0.10,
            format="%.3f",
            help="Approximate long-run expected return (around 10% for the S&P 500).",
        )
        sigma = st.number_input(
            "σ — Annual Volatility",
            min_value=0.001,
            value=0.175,
            format="%.3f",
            help="Annualised standard deviation of returns (for example 0.15–0.20 for a large index).",
        )
        T = st.number_input(
            "T — Time Horizon (years)",
            min_value=0.05,
            value=1.0,
            format="%.2f",
            help="Simulation length in years.",
        )
        steps = st.slider(
            "Steps per Year (granularity)",
            52,
            365,
            365,
            help="365 for daily, 252 for trading days, 52 for weekly.",
        )
        n_paths = st.slider(
            "Number of Paths",
            1,
            500,
            50,
            help="How many independent GBM paths to simulate.",
        )
        use_seed = st.checkbox(
            "Use fixed random seed (72)",
            value=True,
            help="Tick this if you want the same random paths each time.",
        )
        submitted = st.form_submit_button("Run Simulation")

    dt = T / steps
    st.caption(f"Δt (years) is computed automatically: dt = T/steps = {dt:.6f}")

    if st.button("⬅️ Back to Home"):
        go("home")

    # Run simulation when submitted
    if submitted:
        rng = np.random.default_rng(72) if use_seed else np.random.default_rng()
        # shocks for each path and step
        Z = rng.normal(0, 1, size=(n_paths, steps))
        # per-step log returns
        increments = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z
        # cumulative log returns
        log_paths = np.cumsum(increments, axis=1)
        # convert to price paths
        S_paths = S0 * np.exp(np.column_stack([np.zeros(n_paths), log_paths]))

        # store for reuse across tabs
        st.session_state["S_paths"] = S_paths
        st.session_state["stock"] = stock
        st.session_state["S0"] = float(S0)
        st.session_state["T"] = float(T)

    # Show results if they exist
    if "S_paths" in st.session_state:
        S_paths = st.session_state["S_paths"]
        stock_label = (st.session_state.get("stock") or "Selected Stock").strip() or "Selected Stock"
        S0_saved = float(st.session_state.get("S0", 1.0))

        tab_paths, tab_dist, tab_opt, tab_bs, tab_conv = st.tabs(
            [
                "Paths",
                "Terminal Distribution",
                "Option Pricing (Monte Carlo)",
                "Black–Scholes Comparison",
                "Convergence",
            ]
        )

        # Paths Tab
        with tab_paths:
            fig, ax = plt.subplots(figsize=(12, 7))
            for path in S_paths:
                ax.plot(path, alpha=0.9, linewidth=1.5)
            ax.set_title(
                f"Simulated Price Paths for {stock_label} under Geometric Brownian Motion",
                fontsize=20,
                pad=12,
            )
            ax.set_xlabel("Time step", fontsize=14)
            ax.set_ylabel("Price", fontsize=14)
            ax.grid(True, linestyle="--", alpha=0.7)
            ax.set_axisbelow(True)
            ax.xaxis.set_major_locator(ticker.MultipleLocator(25))
            ax.yaxis.set_major_locator(ticker.AutoLocator())
            st.pyplot(fig, clear_figure=True)

        # Terminal Distribution Tab
        with tab_dist:
            ST = S_paths[:, -1]

            mean_ST = float(np.mean(ST))
            median_ST = float(np.median(ST))
            std_ST = float(np.std(ST, ddof=1))
            min_ST = float(np.min(ST))
            max_ST = float(np.max(ST))
            range_ST = max_ST - min_ST
            growth_factor = float(np.mean(ST / S0_saved))
            expected_return = growth_factor - 1.0

            p_up = float(np.mean(ST > S0_saved))
            p_up20 = float(np.mean(ST > 1.2 * S0_saved))
            p_down20 = float(np.mean(ST < 0.8 * S0_saved))

            st.subheader("Summary statistics")
            c1, c2, c3 = st.columns(3)
            c1.metric("Mean terminal price", f"{mean_ST:,.2f}")
            c2.metric("Median", f"{median_ST:,.2f}")
            c3.metric("Standard deviation", f"{std_ST:,.2f}")

            c4, c5, c6 = st.columns(3)
            c4.metric("Minimum", f"{min_ST:,.2f}")
            c5.metric("Maximum", f"{max_ST:,.2f}")
            c6.metric("Range", f"{range_ST:,.2f}")

            c7, c8 = st.columns(2)
            c7.metric("Expected growth factor E[Sₜ/S₀]", f"{growth_factor:,.4f}")
            c8.metric("Expected return E[Sₜ/S₀ − 1]", f"{expected_return*100:,.2f}%")

            st.markdown("**Probabilities from the simulations:**")
            st.write(f"- P(Sₜ > S₀): {p_up*100:.2f}%")
            st.write(f"- P(Sₜ > 1.2 · S₀): {p_up20*100:.2f}%")
            st.write(f"- P(Sₜ < 0.8 · S₀): {p_down20*100:.2f}%")

            st.markdown("---")

            bins = st.slider("Histogram bins", 20, 120, 50)
            density = st.checkbox(
                "Normalise (show density instead of counts)",
                value=False,
            )

            fig2, ax2 = plt.subplots(figsize=(12, 7))
            ax2.hist(ST, bins=bins, edgecolor="white", density=density)
            ax2.set_title(f"Terminal Price Distribution for {stock_label}", fontsize=20, pad=12)
            ax2.set_xlabel("Terminal price", fontsize=14)
            ax2.set_ylabel("Density" if density else "Frequency", fontsize=14)
            ax2.grid(True, linestyle="--", alpha=0.4)
            ax2.set_axisbelow(True)
            st.pyplot(fig2, clear_figure=True)

        # Coming Soon Tabs
        with tab_opt:
            st.subheader("Option Pricing (Monte Carlo)")
            st.info(
                "Coming soon. The idea is to simulate option payoffs under these paths "
                "and estimate prices from the expected discounted payoff."
            )

        with tab_bs:
            st.subheader("Black–Scholes Comparison")
            st.info(
                "Coming soon. I plan to compare Monte Carlo estimates with the analytical "
                "Black–Scholes formula for plain vanilla options."
            )

        with tab_conv:
            st.subheader("Convergence analysis")
            st.info(
                "Coming soon. This page will show how Monte Carlo estimates stabilise as "
                "the number of paths increases."
            )

    else:
        st.info("Fill in the parameters above and click Run Simulation to view paths and the terminal distribution.")