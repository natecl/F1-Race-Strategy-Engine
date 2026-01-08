F1 Race Strategy Engine

A data-driven Formula 1 race strategy system that uses machine learning, probabilistic simulation, and optimization to support real-time race decisions such as when to pit, which tire to choose, and how to manage risk under uncertainty.

This project focuses on decision-making, not just prediction.

Project Overview

Formula 1 strategy is a stochastic, adversarial, and time-dependent problem. Lap times are influenced by tire degradation, traffic, fuel load, pit timing, and random events such as safety cars.

This engine models those dynamics using:

Machine learning for tire degradation

Context-aware race state modeling

Monte Carlo simulation for outcome distributions

Optimization logic to evaluate pit strategies

The goal is to answer questions like:

“Should we pit now or in 5 laps — and what’s the downside risk?”

Core Components
1. Tire Degradation Model (ML Core)

Predicts lap-time loss as tires age.

Inputs

Tire compound

Track

Track temperature

Laps since pit

Fuel proxy (lap number)

Outputs

Expected lap time

Degradation curves

Models

Baseline: XGBoost / LightGBM

Upgrade path: LSTM / temporal Transformer

2. Race State Model (Context Awareness)

Captures non-tire factors that affect lap times and strategy.

Includes:

Pit lane time loss per track

Traffic penalties

Undercut / overcut effects

Safety car probability

This layer connects raw predictions to real race conditions.

3. Monte Carlo Race Simulator

Simulates the remainder of a race thousands of times under uncertainty.

Each simulation samples:

Different pit laps

Tire compound choices

Random safety car events

Stochastic lap-time noise

Outputs

Finishing position distributions

Expected points

Risk metrics (P10 / P50 / P90 outcomes)

4. Strategy Optimizer (Decision Engine)

Evaluates competing strategies using expected value and downside risk.

Answers:

Pit now vs later

Aggressive vs conservative strategies

Risk–reward tradeoffs

Designed to support real-time race decisions.

Project Structure
f1-strategy-engine/
│
├── data/
│   ├── raw/              # Raw lap, tire, and race data
│   └── processed/        # Cleaned, feature-engineered datasets
│
├── models/
│   ├── tire_degradation/ # ML models for lap-time prediction
│   └── race_state/       # Contextual race dynamics
│
├── simulation/
│   └── monte_carlo.py    # Race outcome simulations
│
├── strategy/
│   └── optimizer.py      # Strategy evaluation logic
│
├── notebooks/
│   └── exploration.ipynb # EDA and model validation
│
├── src/
│   └── utils.py
│
├── requirements.txt
└── README.md

Data Sources

Public Formula 1 lap time and race datasets

Tire compound and stint data

Track-specific pit lane timing

Exact sources are documented in the data directory.

Why This Project Matters

This project demonstrates:

Applied machine learning beyond simple prediction

Systems thinking across interacting race dynamics

Probabilistic modeling and uncertainty quantification

Decision optimization under real-world constraints

It sits at the intersection of machine learning, quantitative modeling, simulation, and real-time decision systems.

Future Extensions

Real-time inference during live races

Bayesian safety car modeling

Driver-specific performance models

Reinforcement learning for strategy optimization

Interactive visualization dashboards

Tech Stack

Python, C++

NumPy, Pandas

XGBoost, LightGBM

Scikit-learn

Matplotlib

Status

Active development. Models and simulation logic are being iteratively refined.