import csv
import random
import pandas as pd

# ================================
# STEP 1: Read CSV into dictionary
# ================================
def read_csv_to_dict(file_path):
    program_ratings = {}
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip header
        for row in reader:
            program = row[0]
            ratings = [float(x) for x in row[1:]]
            program_ratings[program] = ratings
    return program_ratings


# Path to CSV file
file_path = 'program_ratings.csv'
program_ratings_dict = read_csv_to_dict(file_path)
ratings = program_ratings_dict

# ================================
# STEP 2: Define GA parameters
# ================================
GEN = 100
POP = 50
CO_R = 0.8
MUT_R = 0.2
EL_S = 2

all_programs = list(ratings.keys())
all_time_slots = list(range(6, 24))  # Time slots from 6AM to 11PM

# ================================
# STEP 3: Define functions
# ================================
def fitness_function(schedule):
    total_rating = 0
    for time_slot, program in enumerate(schedule):
        total_rating += ratings[program][time_slot]
    return total_rating


def initialize_pop(programs, time_slots):
    if not programs:
        return [[]]
    all_schedules = []
    for i in range(len(programs)):
        for schedule in initialize_pop(programs[:i] + programs[i + 1:], time_slots):
            all_schedules.append([programs[i]] + schedule)
    return all_schedules


def finding_best_schedule(all_schedules):
    best_schedule = []
    max_ratings = 0
    for schedule in all_schedules:
        total_ratings = fitness_function(schedule)
        if total_ratings > max_ratings:
            max_ratings = total_ratings
            best_schedule = schedule
    return best_schedule


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


def genetic_algorithm(initial_schedule, generations=GEN, population_size=POP,
                      crossover_rate=CO_R, mutation_rate=MUT_R, elitism_size=EL_S):

    population = [initial_schedule]

    for _ in range(population_size - 1):
        random_schedule = initial_schedule.copy()
        random.shuffle(random_schedule)
        population.append(random_schedule)

    for _ in range(generations):
        new_population = []

        # Elitism
        population.sort(key=lambda s: fitness_function(s), reverse=True)
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

    return population[0]


# ================================
# STEP 4: Run the algorithm
# ================================
print("\nRunning Genetic Algorithm... Please wait.\n")

all_possible_schedules = initialize_pop(all_programs, all_time_slots)
initial_best_schedule = finding_best_schedule(all_possible_schedules)
rem_t_slots = len(all_time_slots) - len(initial_best_schedule)

genetic_schedule = genetic_algorithm(initial_best_schedule, generations=GEN,
                                     population_size=POP, elitism_size=EL_S)

final_schedule = initial_best_schedule + genetic_schedule[:rem_t_slots]

# ================================
# STEP 5: Display Results
# ================================
schedule_data = []
for time_slot, program in enumerate(final_schedule):
    schedule_data.append({
        "Time Slot": f"{all_time_slots[time_slot]:02d}:00",
        "Program": program,
        "Rating": ratings[program][time_slot]
    })

df_schedule = pd.DataFrame(schedule_data)

print("===============================================")
print("📺 FINAL OPTIMAL TV SCHEDULE")
print("===============================================\n")
print(df_schedule.to_string(index=False))
print("\n-----------------------------------------------")
print(f"⭐ Total Ratings: {fitness_function(final_schedule):.2f}")
print(f"📊 Average Rating per Time Slot: {fitness_function(final_schedule)/len(final_schedule):.2f}")
print("-----------------------------------------------")
