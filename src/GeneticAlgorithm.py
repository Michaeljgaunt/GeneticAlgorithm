
import math
import numpy
import random

#Defining the objective function.
def objective_function(x):
    result = x * x
    return result

#Defining a function to randomly generate chromosomes.
def generate_chromosomes(upper_bound, chrom_num):
    #Finding the minimum bit string length needed to hold the upper bound integer.
    bs_length = int(math.ceil(math.log(upper_bound, 2)))
    #Instantiating a list to hold the chromosomes.
    chrom_array = numpy.zeros((chrom_num, bs_length))
    #Iterating up to the number of chromosomes wanted.
    for i in xrange(0, (chrom_num)):
        #Iterating over each bit in the bit string
        for j in xrange(0, (bs_length - 1)):
            #Finding a random integer between 0 and 9 inclusive.
            rand_int = random.randint(0, 9)
            #If the integer is <= 4, the bit in question is assigned a 0.
            if(rand_int <= 4):
                chrom_array[i][j] = 0
            #If the integer is >= 5, the bit in question is assigned a 1.                
            else:
                chrom_array[i][j] = 1
    #The randomised chromosomes are returned in a list.
    print "generate_chromosomes: " + str(list(chrom_array))
    return list(chrom_array)

#Defining a function to convert a bit string into a decimal value.
def convert_bitstring(chrom_array, lower_bound, upper_bound):
    #Finding the number and length of chromosomes
    chrom_num = len(chrom_array)
    chrom_len = len(chrom_array[0])
    #Creating an array to hold the fitness values.
    bs_array = numpy.zeros(chrom_num)
    #Iterating over each chromosome
    for i in xrange(0, chrom_num):
        #Instantiating bit string value as 0, and the power as 0.
        bs_value = 0
        power = 0
        #Iterating over each bit in the bit string, in backwards order.
        for j in xrange((chrom_len), 0, -1):
            #Adding the value of the corresponding bit to the overall bit string value.
            bs_value += chrom_array[i][j - 1] * (2 ** power)
            #Increasing the power
            power +=1
        #Squeezing the bitstring value in between the range given.
        squeezed_value = float(lower_bound) + ( ( float(upper_bound - lower_bound) / (float(2 ** chrom_len) - float(1)) ) * float(bs_value) )
        #Adding the squeezed value into the array
        bs_array[i] = squeezed_value
    #Returning the bit string as decimals in an array
    print "convert_bitstring: " + str(list(bs_array))
    return list(bs_array)
  
#Defining a function to evaluate the fitness of a given variable.        
def evaluate_fitness(decimal_array):
    #Saving the length of the value_array.
    value_array_size = len(decimal_array)
    #Making an array to hold fitness values
    fitness_array = numpy.zeros(value_array_size)
    #Instantiating the sum as 0
    sum = 0
    #Iterating over the length of the value array.
    for i in xrange(0, value_array_size):
        #Saving the current element as x
        x = decimal_array[i]
        #Passing x into the objective function to evaluate it's fitness.
        fitness = objective_function(x)
        #Saving the fitness value in an array.
        fitness_array[i] = fitness
        #Adding it to the sum value.
        sum += fitness
    #Returning the fitness array and the sum.
    print "evaluate fitness: " + str(list(fitness_array))
    return {"fitnesses":fitness_array, "sum":sum}

#Defining a funtion to evaluate the probability of a given variable.
def evaluate_probability(fitness_array, sum):
    #Saving the size of the fitness array
    fitness_array_size = len(fitness_array)
    #Making an array to hold the probability values.
    prob_array = numpy.zeros(fitness_array_size)
    #Iterating over the fitness array
    for i in xrange(0, fitness_array_size):
        #Saving the current element as x.
        x = fitness_array[i]
        #Calculating the probability
        probability = x / sum
        #Saving the probability in the array.
        prob_array[i] = probability
    #Returning the probability array
    print "evaluate_probability: " + str(list(prob_array))
    return list(prob_array)

#Defining a function to rank the chromosomes based on the roulette method using their probabilities.
def roulette_rank(chrom_array, prob_array):
    #Instantiating the total value and current index.
    total = 0
    curr_ind = 0
    #Creating a new array to hold the chosen chromosomes.
    parent_array = []
    #Iterating over the number of chromosomes.
    for i in xrange(0, len(chrom_array)):
        #Generating a random float between 0 and 1.
        random_num = random.random()
        #Adding the current iterating probability to the total.
        total += prob_array[i]
        #Saving the current index.
        curr_ind = 0
        #If the random number is greater than the running total:
        if (random_num >= total):
            #Append the chosen chromosome in the parent array.
            parent_array.append(chrom_array[i])
            #Reset the total to 0.
            total = 0
            continue
    print "roulette_rank: " + str(list(parent_array))
    return parent_array

#Defining a function to perform chromosome crossover.
#def crossover(chrom_array):
    #Saving number of the chromosomes.
 #   chrom_num = len(chrom_array)
    #Saving length of chromosomes.
  #  chrom_len = len(chrom_array[0])
    #making new array to hold child chromosomes.
   # child_array = []
    #Iterating over the number of chromosome pairs.
    #for i in xrange(1, ((chrom_num / 2) + 1)):
     #   chrom_a = chrom_array[(2 * i) - 2]
      #  chrom_b = chrom_array[(2 * i) - 1]
       # print chrom_a
        #print chrom_b

        #cut_point = random.randint(1, (chrom_len - 1))

        #child_a = chrom_a[0:cut_point] + chrom_b[cut_point:]
        #child_b = chrom_b[0:cut_point] + chrom_a[cut_point:]

        #child_array.append(child_a)
        #child_array.append(child_b)

    #return child_array



#Defining a function to randomly mutate bit values in a chromosome according to a given mutation rate.
def mutate(mutation_rate, c_array):
    #Saving the number of chromosomes.
    num_chroms = len(c_array)
    #Saving the length of chromosomes.
    chrom_len = len(c_array[0])
    #Iterating over the number of chromosomes.
    for i in xrange(0, num_chroms):
        #Iterating over each chromosome bit
        for j in xrange(0, chrom_len):
            #Generates a random number based on the given mutation rate.
            mutation = random.randint(0, (100 / mutation_rate))
            #If that number is 1
            if (mutation == 20):
                #The bit at the current position is flipped.
                c_array[i][j] = (1 - c_array[i][j])
    print "mutate: " + str(list(c_array))
    return list(c_array)
    
    
