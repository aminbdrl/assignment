import csv
import random

##################################### DEFINING PARAMETERS AND DATASET ################################################################

# Function to read the CSV file and convert it to the desired format
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

# Path to the CSV file
file_path = 'program_ratings.csv'

# Get the data in the required format
program_ratings_dict = read_csv_to_dict(file_path)

# Sample rating programs dataset for each time slot
ratings = program_ratings_dict

GEN = 200
POP = 100
CO_R = 0.8
MUT_R = 0.2
EL_S = 5

all_programs = list(ratings.keys())
all_time_slots = list(range(6, 24))

######################################### DEFINING FUNCTIONS ########################################################################

# Defining fitness function
def fitness_function(schedule):
    total_rating = 0
    for time_slot, program in enumerate(schedule):
        if time_slot < len(ratings[program]):
            total_rating += ratings[program][time_slot]
    return total_rating

# Create initial random population
def create_random_schedule():
    # Each program can be used multiple times across different time slots
    schedule = [random.choice(all_programs) for _ in all_time_slots]
    return schedule

# Initialize population with random schedules
def initialize_population(population_size):
    return [create_random_schedule() for _ in range(population_size)]

############################################# GENETIC ALGORITHM #############################################################################

# Crossover
def crossover(schedule1, schedule2):
    crossover_point = random.randint(1, len(schedule1) - 2)
    child1 = schedule1[:crossover_point] + schedule2[crossover_point:]
    child2 = schedule2[:crossover_point] + schedule1[crossover_point:]
    return child1, child2

# Mutation
def mutate(schedule):
    schedule = schedule.copy()
    mutation_point = random.randint(0, len(schedule) - 1)
    new_program = random.choice(all_programs)
    schedule[mutation_point] = new_program
    return schedule

# Genetic algorithm
def genetic_algorithm(generations=GEN, population_size=POP, crossover_rate=CO_R, mutation_rate=MUT_R, elitism_size=EL_S):
    
    # Initialize population
    population = initialize_population(population_size)
    
    best_ever_schedule = None
    best_ever_fitness = 0
    
    for generation in range(generations):
        # Evaluate fitness for all schedules
        fitness_scores = [(schedule, fitness_function(schedule)) for schedule in population]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Track best schedule ever found
        if fitness_scores[0][1] > best_ever_fitness:
            best_ever_fitness = fitness_scores[0][1]
            best_ever_schedule = fitness_scores[0][0].copy()
        
        # Print progress every 20 generations
        if generation % 20 == 0:
            print(f"Generation {generation}: Best Fitness = {fitness_scores[0][1]:.2f}")
        
        new_population = []
        
        # Elitism - keep best schedules
        new_population.extend([schedule for schedule, _ in fitness_scores[:elitism_size]])
        
        # Create new population through crossover and mutation
        while len(new_population) < population_size:
            # Tournament selection
            parent1 = random.choice(fitness_scores[:population_size//2])[0]
            parent2 = random.choice(fitness_scores[:population_size//2])[0]
            
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
    
    return best_ever_schedule

##################################################### RESULTS ###################################################################################

print("Starting Genetic Algorithm...")
print(f"Programs: {len(all_programs)}, Time Slots: {len(all_time_slots)}")
print(f"Generations: {GEN}, Population: {POP}\n")

# Run genetic algorithm
optimal_schedule = genetic_algorithm(generations=GEN, population_size=POP, elitism_size=EL_S)

print("\n" + "="*60)
print("FINAL OPTIMAL SCHEDULE:")
print("="*60)
for time_slot_idx, program in enumerate(optimal_schedule):
    time = all_time_slots[time_slot_idx]
    rating = ratings[program][time_slot_idx] if time_slot_idx < len(ratings[program]) else 0
    print(f"Time Slot {time:02d}:00 - Program: {program:20s} (Rating: {rating:.2f})")

print("="*60)
print(f"TOTAL RATINGS: {fitness_function(optimal_schedule):.2f}")
print("="*60)
