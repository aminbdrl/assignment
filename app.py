import streamlit as st
import csv
import random
import pandas as pd

# ==============================================
# READ CSV FUNCTION
# ==============================================
def read_csv_to_dict(file_path):
    program_ratings = {}
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            program = row[0]
            ratings = [float(x) for x in row[1:]]
            program_ratings[program] = ratings
    return program_ratings


# ==============================================
# STREAMLIT USER INTERFACE
# ==============================================
st.title("📺 Program Scheduling using Genetic Algorithm")

st.sidebar.header("⚙️ GA Parameter Settings")
CO_R = st.sidebar.slider("Crossover Rate (CO_R)", 0.0, 0.95, 0.8, 0.05)
MUT_R = st.sidebar.slider("Mutation Rate (MUT_R)", 0.01, 0.05, 0.02, 0.01)

GEN = 100
POP = 50
EL_S = 2

file_path = 'program_ratings_modified.csv'
ratings = read_csv_to_dict(file_path)

all_programs = list(ratings.keys())
all_time_slots = list(range(6, 24))  # Time slots from 6:00 to 23:00


# ==============================================
# FITNESS FUNCTION
# ==============================================
def fitness_function(schedule):
    total_rating = 0
    for time_slot, program in enumerate(schedule):
        total_rating += ratings[program][time_slot]
    return total_rating


# ==============================================
# GENETIC ALGORITHM FUNCTIONS
# ==============================================
def crossover(schedule1, schedule2):
    crossover_point = random.randint(1, len(schedule1) - 2)
    child1 = schedule1[:crossover_point] + schedule2[crossover_point:]
    child2 = schedule2[:crossover_point] + schedule1[crossover_point:]
    return child1, child2

def mutate(schedule):
    mutation_point = random.randint(0, len(schedule) - 1)
    new_program = random.choice(all_programs)
    schedule[mutation_point] = new_program
    return schedule

def genetic_algorithm(initial_schedule, generations=GEN, population_size=POP, crossover_rate=CO_R, mutation_rate=MUT_R, elitism_size=EL_S):
    population = [initial_schedule]
    for _ in range(population_size - 1):
        random_schedule = initial_schedule.copy()
        random.shuffle(random_schedule)
        population.append(random_schedule)

    for _ in range(generations):
        new_population = []
        population.sort(key=lambda schedule: fitness_function(schedule), reverse=True)
        new_population.extend(population[:elitism_size])

        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population, k=2)
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()

            if random.random() < mutation_rate:
                child1 = mutate(child1)
            if random.random() < mutation_rate:
                child2 = mutate(child2)

            new_population.extend([child1, child2])

        population = new_population

    population.sort(key=lambda schedule: fitness_function(schedule), reverse=True)
    return population[0]


# ==============================================
# STREAMLIT OUTPUT SECTION
# ==============================================
if st.button("🚀 Generate Optimal Schedule"):
    initial_schedule = all_programs.copy()
    random.shuffle(initial_schedule)
    best_schedule = genetic_algorithm(initial_schedule, crossover_rate=CO_R, mutation_rate=MUT_R)

    total_rating = fitness_function(best_schedule)

    # Display results in table format
    df_schedule = pd.DataFrame({
        "Time Slot": [f"{t:02d}:00" for t in all_time_slots],
        "Selected Program": best_schedule,
    })

    st.success(f"✅ Highest Total Rating: {total_rating:.2f}")
    st.write("### 🕒 Optimized TV Schedule")
    st.dataframe(df_schedule)

    # Download button for results
    st.download_button(
        label="💾 Download Schedule (CSV)",
        data=df_schedule.to_csv(index=False).encode('utf-8'),
        file_name='optimized_schedule.csv',
        mime='text/csv'
    )

st.caption("Developed for JIE42903 Assignment – Evolutionary Algorithm Scheduling")
