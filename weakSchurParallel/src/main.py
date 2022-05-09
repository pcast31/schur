from weak_schur import * 

# Loading the 6-color partition, and testing it.
with open("data/partition6.json", "r", encoding="utf-8") as fp:
    partition6 = json.loads(fp.read())
print(f"Fitness of the 6-color partition = {fitness(partition6)}")

# Now test-driving the generate_partition function using
# user inputs.
num_elems, num_color = [
    int(x) for x in input("Enter max. numbers and number of colors: ").split()
]

# # Allowing the user to choose which algorithm to use.
choice_fitness = int(input("Choose \n(1) Naive fitness \n(2) Iterative Fitness \n(3) Multiproc \n:: "))

# # and which choice function to use.
# choice_fn_choice = int(input("Choose (1) Min choice or (2) MinRandom: "))
# choice_fn = np.argmin if choice_fn_choice == 1 else choice.min_random

choice_fn = np.argmin # Hardlock for now
# Now calling the chosen functions based on user input
if choice_fitness == 1:
    result = generate_partition(
        num_colors=num_color, max_num=num_elems, fitness_choice=choice_fn
    )
elif choice_fitness == 2:
    result = generate_partition_iterative(
        num_colors=num_color, max_num=num_elems, fitness_choice=choice_fn
    )
elif choice_fitness == 3: 
    result = generate_partition_multiproc(
        num_colors=num_color, max_num=num_elems, fitness_choice=choice_fn
    )
else:
    print(f"Wrong fitness_choice ({choice_fitness}) was entered. Please try again.")
