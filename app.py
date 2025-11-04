# ==========================================
# Streamlit App: Scheduling using Genetic Algorithm
# ==========================================

import streamlit as st
import pandas as pd
import numpy as np
import random

# ------------------------------------------
# 1. Load Dataset
# ------------------------------------------
st.title("📺 TV Program Scheduling using Genetic Algorithm")

st.markdown("""
This application uses a **Genetic Algorithm (GA)** to schedule TV programs based on their ratings.  
You can test **three different trials** with various combinations of **Crossover Rate (CO_R)** and **Mutation Rate (MUT_R)** 
to see how they affect the resulting schedule.
""")

# Load CSV (use the modified file)
@st.cache_data
def load_data():
    df = pd.read_csv("program_ratings_modified.csv")
    return df

df = load_data()
st.subheader("📊 Program Rating Data")
st.dataframe(df)

programs = df["Type of Program"].tolist()
hours = df.columns[1:]

# ------------------------------------------
# 2. GA Parameters for 3 Trials
# ------------------------------------------
st.sidebar.header("⚙️ Genetic Algorithm Parameters (for 3 Trials)")

st.sidebar.markdown("### Trial 1")
CO_R1 = st.sidebar.slider("Crossover Rate (CO_R1)", 0.0, 0.95, 0.8, 0.05)
MUT_R1 = st.sidebar.slider("Mutation Rate (MUT_R1)", 0.01, 0.05, 0.2, 0.01)  # ✅ Default 0.2

st.sidebar.markdown("### Trial 2")
CO_R2 = st.sidebar.slider("Crossover Rate (CO_R2)", 0.0, 0.95, 0.6, 0.05)
MUT_R2 = st.sidebar.slider("Mutation Rate (MUT_R2)", 0.01, 0.05, 0.03, 0.01)

st.sidebar.markdown("### Trial 3")
CO_R3 = st.sidebar.slider("Crossover Rate (CO_R3)", 0.0, 0.95, 0.9, 0.05)
MUT_R3 = st.sidebar.slider("Mutation Rate (MUT_R3)", 0.01, 0.05, 0.04, 0.01)

POP_SIZE = 10
GENERATIONS = 20

# ------------------------------------------
# 3. Genetic Algorithm Functions
# ------------------------------------------
def fitness(schedule, df):
    """Calculate total rating for a given schedule."""
    total = 0
    for h, prog in enumerate(schedule):
        total += df.loc[df["Type of Program"] == prog, df.columns[h + 1]].values[0]
    return total

def selection(population, fitnesses):
    """Roulette-wheel selection based on fitness."""
    total_fit = sum(fitnesses)
    probs = [f / total_fit for f in fitnesses]
    return population[np.random.choice(len(population), p=probs)]

def crossover(parent1, parent2, rate):
    """Single-point crossover."""
    if random.random() < rate:
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    return parent1, parent2

def mutate(schedule, rate):
    """Randomly mutate some genes in the schedule."""
    for i in range(len(schedule)):
        if random.random() < rate:
            schedule[i] = random.choice(programs)
    return schedule

def genetic_algorithm(df, CO_R, MUT_R, pop_size=POP_SIZE, generations=GENERATIONS):
    """Run the genetic algorithm for the scheduling problem."""
    population = [random.choices(programs, k=len(hours)) for _ in range(pop_size)]

    for _ in range(generations):
        fitnesses = [fitness(ind, df) for ind in population]
        new_population = []

        while len(new_population) < pop_size:
            p1 = selection(population, fitnesses)
            p2 = selection(population, fitnesses)
            c1, c2 = crossover(p1, p2, CO_R)
            c1 = mutate(c1, MUT_R)
            c2 = mutate(c2, MUT_R)
            new_population += [c1, c2]

        population = new_population[:pop_size]

    best = max(population, key=lambda x: fitness(x, df))
    best_fit = fitness(best, df)
    return best, best_fit

# ------------------------------------------
# 4. Run All 3 Trials
# ------------------------------------------
if st.button("🚀 Run Genetic Algorithm for All Trials"):

    # Trial 1
    best1, fit1 = genetic_algorithm(df, CO_R1, MUT_R1)
    result1 = pd.DataFrame({"Hour": hours, "Program": best1})

    # Trial 2
    best2, fit2 = genetic_algorithm(df, CO_R2, MUT_R2)
    result2 = pd.DataFrame({"Hour": hours, "Program": best2})

    # Trial 3
    best3, fit3 = genetic_algorithm(df, CO_R3, MUT_R3)
    result3 = pd.DataFrame({"Hour": hours, "Program": best3})

    # Display results
    st.subheader("📊 Trial 1 Results")
    st.write(f"**Crossover Rate:** {CO_R1}, **Mutation Rate:** {MUT_R1}")
    st.write(f"**Total Fitness:** {fit1:.2f}")
    st.dataframe(result1)

    st.subheader("📊 Trial 2 Results")
    st.write(f"**Crossover Rate:** {CO_R2}, **Mutation Rate:** {MUT_R2}")
    st.write(f"**Total Fitness:** {fit2:.2f}")
    st.dataframe(result2)

    st.subheader("📊 Trial 3 Results")
    st.write(f"**Crossover Rate:** {CO_R3}, **Mutation Rate:** {MUT_R3}")
    st.write(f"**Total Fitness:** {fit3:.2f}")
    st.dataframe(result3)

    # Compare summary
    summary = pd.DataFrame({
        "Trial": ["Trial 1", "Trial 2", "Trial 3"],
        "Crossover Rate": [CO_R1, CO_R2, CO_R3],
        "Mutation Rate": [MUT_R1, MUT_R2, MUT_R3],
        "Total Fitness": [fit1, fit2, fit3]
    })
    st.subheader("📈 Summary Comparison of All Trials")
    st.dataframe(summary)
