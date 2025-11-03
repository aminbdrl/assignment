import streamlit as st
import pandas as pd
import csv
import random
import matplotlib.pyplot as plt

# ================================
# STREAMLIT APP HEADER
# ================================
st.set_page_config(page_title="TV Scheduling Optimizer", layout="wide")
st.title("📺 TV Scheduling Optimization using Genetic Algorithm")
st.write("Upload your CSV file containing program ratings by time slot, and the app will find the optimal TV schedule for maximum total ratings.")

# ================================
# UPLOAD CSV
# ================================
uploaded_file = st.file_uploader("program_ratings.csv", type=["csv"])

if uploaded_file is not None:
    # Read CSV into dictionary
    def read_csv_to_dict(file):
        program_ratings = {}
        reader = csv.reader(file.read().decode('utf-8').splitlines())
        header = next(reader)
        for row in reader:
            program = row[0]
            ratings = [float(x) for x in row[1:]]
            program_ratings[program] = ratings
        return program_ratings

    program_ratings_dict = read_csv_to_dict(uploaded_file)
    ratings = program_ratings_dict

    # ================================
    # PARAMETERS
    # ================================
    GEN = st.sidebar.number_input("Generations", 10, 500, 100)
    POP = st.sidebar.number_input("Population Size", 10, 200, 50)
    CO_R = st.sidebar.slider("Crossover Rate", 0.0, 1.0, 0.8)
    MUT_R = st.sidebar.slider("Mutation Rate", 0.0, 1.0, 0.2)
    EL_S = st.sidebar.number_input("Elitism Size", 1, 10, 2)

    all_programs = list(ratings.keys())
    all_time_slots = list(range(6, 24))  # 6 AM to 11 PM

    # ================================
    # FITNESS FUNCTION
    # ================================
    def fitness_function(schedule):
        total_rating = 0
        for time_slot, program in enumerate(schedule):
            total_rating += ratings[program][time_slot]
        return total_rating

    # ================================
    # INITIALIZATION
    # ================================
    def initialize_population(programs, size):
        population = []
        for _ in range(size):
            schedule = random.sample(programs, len(programs))
            population.append(schedule)
        return population

    # ================================
    # GENETIC OPERATORS
    # ================================
    def crossover(parent1, parent2):
        point = random.randint(1, len(parent1) - 2)
        child1 = parent1[:point] + [p for p in parent2 if p not in parent1[:point]]
        child2 = parent2[:point] + [p for p in parent1 if p not in parent2[:point]]
        return child1, child2

    def mutate(schedule):
        i, j = random.sample(range(len(schedule)), 2)
        schedule[i], schedule[j] = schedule[j], schedule[i]
        return schedule

    # ================================
    # GENETIC ALGORITHM
    # ================================
    def genetic_algorithm(generations, population_size, crossover_rate, mutation_rate, elitism_size):
        population = initialize_population(all_programs, population_size)

        for _ in range(generations):
            population = sorted(population, key=lambda s: fitness_function(s), reverse=True)
            new_population = population[:elitism_size]

            while len(new_population) < population_size:
                parent1, parent2 = random.choices(population[:10], k=2)
                if random.random() < crossover_rate:
                    child1, child2 = crossover(parent1, parent2)
                else:
                    child1, child2 = parent1.copy(), parent2.copy()

                if random.random() < mutation_rate:
                    child1 = mutate(child1)
                if random.random() < mutation_rate:
                    child2 = mutate(child2)

                new_population.extend([child1, child2])

            population = new_population[:population_size]

        return sorted(population, key=lambda s: fitness_function(s), reverse=True)[0]

    # ================================
    # RUN THE ALGORITHM
    # ================================
    if st.button("🚀 Run Optimization"):
        best_schedule = genetic_algorithm(GEN, POP, CO_R, MUT_R, EL_S)
        total_rating = fitness_function(best_schedule)
        avg_rating = total_rating / len(best_schedule)

        # Prepare dataframe for display
        df = pd.DataFrame({
            "Time Slot": [f"{t:02d}:00" for t in all_time_slots],
            "Program": best_schedule,
            "Rating": [ratings[p][i] for i, p in enumerate(best_schedule)]
        })

        st.subheader("✅ Optimal TV Schedule")
        st.dataframe(df, use_container_width=True)

        st.write(f"**⭐ Total Ratings:** {total_rating:.2f}")
        st.write(f"**📊 Average Rating per Slot:** {avg_rating:.2f}")

        # ================================
        # VISUALIZATION
        # ================================
        st.subheader("📈 Ratings by Time Slot")
        fig, ax = plt.subplots()
        ax.plot(df["Time Slot"], df["Rating"], marker='o')
        ax.set_xlabel("Time Slot")
        ax.set_ylabel("Rating")
        ax.set_title("Program Ratings per Time Slot")
        plt.xticks(rotation=45)
        st.pyplot(fig)

else:
    st.info("👆 Please upload your `program_ratings.csv` file to start.")
