import numpy as np
from numpy import loadtxt
import pygad

def st_array(string, sep):
    sep_lis=list(list(string.split(sep)))
    io=[]
    for i in range(0,len(sep_lis)):
        io.append(int(sep_lis[i]))
    return io

file = open('23.txt','r')
first_str =  st_array(file.readline(),' ')
file.close()

weight, value, capacity = loadtxt("23.txt",dtype='float', comments="#", delimiter=" ",skiprows=1, unpack=True)

knapsack_0 = int(first_str[0])   #Макс вес который может выдержать сумка
knapsack_1 = int(first_str[1]) #макс емкость

item_list = np.zeros((len(weight),3))
for i in range(len(weight)):
        item_list[i,0] = weight[i]
        item_list[i,1] = value[i]
        item_list[i,2] = capacity[i]


function_inputs = item_list

def cal_fitness(solution, solution_idx):
    a1 = 0.0
    a2 = 0.0
    a3 = 0.0
    for i in range(len(solution)):
        a1 += solution[i] * value[i]
        a2 += solution[i] * weight[i]
        a3 += solution[i] * capacity[i]
    if a2 <= knapsack_0 and a1 <= knapsack_1:
        fit = a3
    else :
        fit = 0
    return fit

num_generations = 100 # Количество поколений
num_parents_mating = 20 # Количество решений которые можно выбрать в качестве родителей

sol_per_pop = 200 # Количество решений в популяции.
num_genes = len(function_inputs) #Количество генов равно количеству элементов



parent_selection_type = "rws" # Тип родительского выбора
keep_parents = 1 # Число родителей которых нужно оставить в след популяции

crossover_type = "single_point" # Тип оператора

# Параметры операции мутации.
mutation_type = "random" # Тип оператора мутации.
mutation_percent_genes = 20 # Процент генов, подлежащих мутации

last_fitness = 0
def callback_generation(ga_instance):
    global last_fitness
    print("Generation = {generation}".format(generation=ga_instance.generations_completed))
    print("Fitness    = {fitness}".format(fitness=ga_instance.best_solution()[1]))
    print("Change     = {change}".format(change=ga_instance.best_solution()[1] - last_fitness))
    last_fitness = ga_instance.best_solution()[1]

# Создание экземпляра класса
ga_instance = pygad.GA(num_generations=50,
                       num_parents_mating=40, #20% популяции
                       fitness_func=cal_fitness,
                       sol_per_pop=200,
                       num_genes=len(function_inputs),
                       gene_type=np.int16,
                       init_range_low=0,
                       init_range_high=2,
                       parent_selection_type=parent_selection_type,
                       keep_parents=40, #20% популяции
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       mutation_percent_genes=mutation_percent_genes,
                       callback_generation=callback_generation)

#  Запуск GA для оптимизации параметров функции.
ga_instance.run()

# После завершения поколений отображаются некоторые графики,
ga_instance.plot_result()

# Возвращение лучшего решения..
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))


if ga_instance.best_solution_generation != -1:
    print("Best fitness value reached after {best_solution_generation} generations.".format(best_solution_generation=ga_instance.best_solution_generation))

print('№   Вес   Объем  Ценность')
total_weight = 0.0
total_value = 0.0
for i in range(len(solution)):
    total_value += solution[i] * value[i]
    total_weight += solution[i] * weight[i]
    if solution[i]==1 : 
        print('{0} {1} {2} {3}\n'.format(i, weight[i], value[i],capacity[i],))
print("Вес:", total_weight,"Объем:", total_value,"Ценность:", solution_fitness)