import streamlit as st
import pandas as pd
import numpy as np
import random

# ------------------------------------------
# 1. Load Dataset
# ------------------------------------------
st.title("📺 TV Program Scheduling using Genetic Algorithm")

st.markdown("""
Aplikasi ini menggunakan **Genetic Algorithm (GA)** untuk menjadualkan program berdasarkan rating.
Anda boleh ubah **Crossover Rate (CO_R)** dan **Mutation Rate (MUT_R)** untuk lihat kesan terhadap hasil jadual.
""")

# Load CSV (gunakan fail yang telah diubah)
@st.cache_data
def load_data():
    df = pd.read_csv("program_ratings_modified.csv")
    return df

df = load_data()
st.subheader("📊 Data Rating Program (Dari CSV)")
st.dataframe(df)

programs = df["Type of Program"].tolist()
hours = df.columns[1:]

# ------------------------------------------
# 2. Parameter Input
# ------------------------------------------
st.sidebar.header("⚙️ Genetic Algorithm Parameters")
CO_R = st.sidebar.slider("Crossover Rate (CO_R)", 0.0, 0.95, 0.8)
MUT_R = st.sidebar.slider("Mutation Rate (MUT_R)", 0.01, 0.05, 0.02)
POP_SIZE = 10
GENERATIONS = 20

# ------------------------------------------
# 3. Genetic Algorithm Functions
# ------------------------------------------
def fitness(schedule, df):
    # Kira jumlah rating untuk jadual tertentu
    total = 0
    for h, prog in enumerate(schedule):
        total += df.loc[df["Type of Program"] == prog, df.columns[h + 1]].values[0]
    return total

def selection(population, fitnesses):
    total_fit = sum(fitnesses)
    probs = [f / total_fit for f in fitnesses]
    return population[np.random.choice(len(population), p=probs)]

def crossover(parent1, parent2, rate):
    if random.random() < rate:
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    return parent1, parent2

def mutate(schedule, rate):
    for i in range(len(schedule)):
        if random.random() < rate:
            schedule[i] = random.choice(programs)
    return schedule

# ------------------------------------------
# 4. GA Main Loop
# ------------------------------------------
def genetic_algorithm(df, CO_R, MUT_R, pop_size=POP_SIZE, generations=GENERATIONS):
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
# 5. Run GA & Display Results
# ------------------------------------------
if st.button("🚀 Jalankan Genetic Algorithm"):
    best_schedule, best_fitness = genetic_algorithm(df, CO_R, MUT_R)

    st.success(f"✅ Jadual terbaik dijumpai dengan fitness: {best_fitness:.2f}")
    result = pd.DataFrame({
        "Hour": hours,
        "Program": best_schedule
    })

    st.subheader("📅 Jadual Siaran Terbaik")
    st.dataframe(result)

    st.write("**Parameter Digunakan:**")
    st.write(f"- Crossover Rate: {CO_R}")
    st.write(f"- Mutation Rate: {MUT_R}")
