import streamlit as st
import csv
import random
import pandas as pd

# ============================================
# 1. Load CSV File
# ============================================
def read_csv_to_dict(file_path):
    program_ratings = {}
    
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            program = row[0]
            ratings = [float(x) for x in row[1:]]
            program_ratings[program] = ratings
    return program_ratings, header[1:]

# File path (use relative path for Streamlit)
file_path = "program_ratings_modified.csv"
ratings, hours = read_csv_to_dict(file_path)

all_programs = list(ratings.keys())
all_time_slots = hours  # use CSV header as time slots

# ============================================
# 2. GA Parameters (Sidebar)
# ============================================
st.title("📺 TV Program Scheduling using Genetic Algorithm")
st.sidebar.header("⚙️ GA Parameters")

GEN = st.sidebar.slider("Generations", 10, 200, 50)
POP = st.sidebar.slider("Population Size", 10, 100, 30)
CO_R = st.sidebar.slider("Crossover Rate", 0.0, 1.0, 0.8)
MUT_R = st.sidebar.slider("Mutation Rate", 0.0, 1.0, 0.2)
EL_S = st.sidebar.slider("Elitism Size", 1, 5, 2)

# ============================================
# 3. Fitness Function
# ============================================
def fitness_function(schedule):
    total_rating = 0
    for time_slot, program in enumerate(schedule):
        total_rating += ratings[program][time_slot]
    return total_rating

# ============================================
# 4. Genetic Algorithm Components
# ============================================
def initialize_population(pop_size):
    population = []
    for _ in range(pop_size):
        population.append(random.sample(all_programs, len(all_programs)))
    return population

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 2)
    child1 = parent1[:point] + [p for p in parent2 if p not in parent1[:point]]
    child2 = parent2[:point] + [p for p in parent1 if p not in parent2[:point]]
    return child1, child2

def mutate(schedule):
    i, j = random.sample(range(len(schedule)), 2)
    schedule[i], schedule[j] = schedule[j], schedule[i]
    return schedule

def genetic_algorithm():
    population = initialize_population(POP)

    for _ in range(GEN):
        population = sorted(population, key=lambda x: fitness_function(x), reverse=True)
        new_population = population[:EL_S]

        while len(new_population) < POP:
            parent1, parent2 = random.choices(population[:10], k=2)
            if random.random() < CO_R:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()

            if random.random() < MUT_R:
                child1 = mutate(child1)
            if random.random() < MUT_R:
                child2 = mutate(child2)

            new_population += [child1, child2]

        population = new_population[:POP]

    best = max(population, key=lambda x: fitness_function(x))
    return best, fitness_function(best)

# ============================================
# 5. Run Algorithm and Display Results
# ============================================
if st.button("🚀 Run Genetic Algorithm"):
    best_schedule, best_score = genetic_algorithm()

    st.success(f"✅ Best schedule found with total rating: {best_score:.2f}")

    result_df = pd.DataFrame({
        "Hour": all_time_slots,
        "Program": best_schedule
    })

    st.subheader("📅 Optimal TV Schedule")
    st.dataframe(result_df)
