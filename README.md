# Monte Carlo Stock & Option Simulator

Interactive Python app built with **Streamlit**, modelling stock prices under **Geometric Brownian Motion (GBM)** and visualising multiple stochastic paths. The simulator demonstrates the use of **Monte Carlo methods** in financial modelling, exploring randomness, volatility, and expected return in a controlled, data-driven environment.

---

## 🎯 Features
- Adjustable parameters: initial price (S₀), drift (μ), volatility (σ), time horizon (T), number of steps, and number of paths.
- Dynamic visualisation of simulated price paths under GBM.
- Terminal price distribution histogram with key summary statistics:
  - Mean, median, standard deviation, min/max, range
  - Expected growth and return
  - Probability of exceeding or falling below thresholds
- Clean interface with organised tabs for simulation and analysis.
- Placeholder tabs for upcoming modules:
  - Monte Carlo Option Pricing
  - Black–Scholes Analytical Comparison
  - Convergence Analysis
- Built with **Streamlit**, **NumPy**, and **Matplotlib**.

---

## ⚙️ Requirements
- **Python 3.8 or later**
- Dependencies:
  - Streamlit  
  - NumPy  
  - Matplotlib  

Install the dependencies directly using:
```
pip install streamlit numpy matplotlib
```

---

## ▶️ Running the Simulator
Follow these steps to launch the casino:

1. **Download the project**
   - Click the green **Code** button above and select **Download ZIP**
   - Or clone it via terminal:
```
git clone https://github.com/lucakukha/monte-carlo-stock-option-simulator.git
```

2. **Install dependencies**

Open a terminal or command prompt in this folder and run:
```
pip install streamlit numpy matplotlib
```
3. **Running the simulator**

In the same terminal and directory, run:
```
streamlit run monte_carlo_simulator.py
```
Streamlit will open in a browser window with the Monte Carlo Stock & Option Simulator.  
Double click on "Simulate Stock Paths" to get started
