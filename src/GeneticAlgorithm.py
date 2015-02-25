
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
    #Returning the bit string as decimals in an array.
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
    return list(prob_array)

#Defining a function to match chromosomes and perform chromosome crossover.
def crossover(chrom_array, prob_array):
    #Copying the chromosomes and probabilities into a new array.
    copied_chrom_array = chrom_array
    copied_prob_array = prob_array
    #Saving the number of chromosomes.
    num_chroms = len(copied_chrom_array)
    #Defining an array to hold the parents undergoing crossover.
    crossover_array = [0, 0]
    #Defining an array to hold the child chromosomes
    child_chrom_array = []

    #Iterating over chromosome pairs.
    for k in xrange(0, (num_chroms / 2)):
        #Iterating twice
        for i in xrange(0 ,2):
            #Finding the index of the maximum probability.
            max_index = copied_prob_array.index(max(copied_prob_array))
            #Using that to index into the chromosome array and copy it into the crossover array.
            crossover_array[i] = copied_chrom_array[max_index]
            #Delete the chromosome and corresponding probability from the original chromosome array and the probability array
            del copied_chrom_array[max_index]
            del copied_prob_array[max_index]

        #Generating a random cut point on the chromosomes.
        cut_point = random.randint(1, 4)
        #Iterating up to the cut point.
        for i in xrange(0, cut_point):
            #Saving the bit value from each chromosome to a temporary variable.
            temp_bit_1 = crossover_array[0][i]
            temp_bit_2 = crossover_array[1][i]
            #Swapping the chromosome's bit variables (i..e crossover)
            crossover_array[0][i] = temp_bit_2
            crossover_array[1][i] = temp_bit_1
        #Appending the new children chromosomes in the child array.
        child_chrom_array.append(crossover_array[0])
        child_chrom_array.append(crossover_array[1])
    #Returning the child array.
    return child_chrom_array

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
    return list(c_array)
    
    
