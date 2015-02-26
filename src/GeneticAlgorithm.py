
import math
import numpy
import random

#Defining the objective function.
def objective_function(x):
    #result = (x * (math.sin(x) * (math.pi * 10)))
    result = x * x * x
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
    #Returning the bit string as decimals in an array
    return list(bs_array)

#Defining a function to evaluate the fitness of a given variable.        
def evaluate_fitness(value_array):
    #Saving the length of the value_array.
    value_array_size = len(value_array)
    #Making an array to hold fitness values
    fitness_array = numpy.zeros(value_array_size)
    #Instantiating the sum as 0
    sum = 0
    #Iterating over the length of the value array.
    for i in xrange(0, value_array_size):
        #Saving the current element as x
        x = value_array[i]
        #Passing x into the objective function to evaluate it's fitness.
        fitness = objective_function(x)
        #Saving the fitness value in an array.
        fitness_array[i] = fitness
        #Adding it to the sum value.
        sum += fitness
    #Returning the fitness array and the sum.
    return {"fitnesses":list(fitness_array), "sum":sum}

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

#Defining a function to rank the chromosomes based on the roulette method using their probabilities.
def roulette_rank(chrom_array, prob_array):
    #Instantiating the total value.
    total = 0
    #Creating a new array to hold the chosen chromosomes.
    parent_array = []
    #Generating a random float between 0 and 1.
    random_num = random.random()
    #Iterating over the number of chromosomes.
    for i in xrange(0, len(chrom_array)):
        #If the parent array is not empty:
        if(parent_array):
            #Iterating over the number of chromosomes.
            for i in xrange(0, len(chrom_array)):
                #Adding the current iterating probability to the total.
                total += prob_array[i]
                #If the total is greater than the random number:
                if (total >= random_num):
                    #Append the chosen chromosome in the parent array.
                    parent_array.append(chrom_array[i])
                    #Reset the total to 0.
                    total = 0
                    #Generating a new random number
                    random_num = random.random()
                    #Breaking into the outer for loop.
                    break
        #If the parent array is empty:
        else:
            #Finding the index of the best chromosome.
            best_index = prob_array.index(max(prob_array))
            #Appending the best chromosome in the parent array to ensure its survival.
            parent_array.append(chrom_array[best_index])
    return parent_array

def crossover(chrom_array):
    #Saving number of the chromosomes.
    chrom_num = len(chrom_array)
    #Saving length of chromosomes.
    chrom_len = len(chrom_array[0])
    #making new array to hold child chromosomes.
    child_array = []
    #Iterating over the number of chromosome pairs.
    for i in xrange(1, ((chrom_num / 2) + 1)):
        #Getting the chromosomes in the pair.
        chrom_a = chrom_array[(2 * i) - 2]
        chrom_b = chrom_array[(2 * i) - 1]
        #Randomly generating a cut point.
        cut_point = random.randint(1, (chrom_len - 1))
        #Cutting both chromosomes and combining the segments (one from each parent). Saving as a new chromosome.
        child_a = list(chrom_a[0:cut_point]) + list(chrom_b[cut_point:])
        child_b = list(chrom_b[0:cut_point]) + list(chrom_a[cut_point:])
        #Appending the two child chromosomes in the child array.
        child_array.append(child_a)
        child_array.append(child_b)
    #Returning the child chromosomes.
    return child_array

#Defining a function to randomly mutate bit values in a chromosome according to a given mutation rate.
def mutate(mutation_rate, chrom_array):
    #Saving the number of chromosomes.
    num_chroms = len(chrom_array)
    #Saving the length of chromosomes.
    chrom_len = len(chrom_array[0])
    #Iterating over the number of chromosomes.
    for i in xrange(0, num_chroms):
        #Iterating over each chromosome bit
        for j in xrange(0, chrom_len):
            #Generates a random number based on the given mutation rate.
            mutation = random.randint(0, (100 / mutation_rate))
            #If that number is 1
            if (mutation == 1):
                #The bit at the current position is flipped.
                chrom_array[i][j] = (1 - chrom_array[i][j])
    return list(chrom_array)

#Defining a function to aid in debugging.
def debug():
    print "----------------------------------- DEBUG MODE ---------------------------------------"
    print "| Generating 4 chromosomes of length 5.                                              |"                                     
    print "| Squeezing with a range of 2 - 60                                                   |"
    print "| Iterating 3 times.                                                                 |"
    print "| Mutation rate is 50%.                                                              |"
    print "|                                                                                    |"
    print "| The debug statements are printed in the order that the functions are               |"
    print "| called in __main__                                                                 |"
    print "|                                                                                    |"
    print "| Layout:                                                                            |"
    print "| [Description of event] [Possible errors to check] (corresponding function name):   |"
    print "| [values returned by function]                                                      |"
    print "--------------------------------------------------------------------------------------\n"
    
    #Generating 4 chromosomes that hold a 5-bit bitstring.
    chromosomes = generate_chromosomes(31, 4)
    print "\n[Randomly generating first set of chromosomes] [Check that there are 4 chromosomes of length 5] (generate_chromosomes): "
    print str(chromosomes) 
    print ""
    print ""
    
    #Iterating the algorithm 5 times.
    for i in xrange(0, 3):
        print "\nBeginning iteration " + str(i + 1) + "."

        #Calculating the decimal values of the bit string chromosomes, squeezing in a range of 2-60.
        chromosome_values = convert_bitstring(chromosomes, 2, 60)
        print "\n[Converting to decimals] [Check the values are squeezed within the bounds] (convert_bitstring): " 
        print str(chromosome_values)
        #Evaluating the chromosomes' fitness and summing their values.
        chromosome_evaluation = evaluate_fitness(chromosome_values)
        chromosome_fitnesses = chromosome_evaluation.get("fitnesses")
        print "\n[Evaluating fitnesses] [n/a] (evaluate_fitness): "
        print str(chromosome_fitnesses)
        chromosome_fitness_sum = chromosome_evaluation.get("sum")
        print "\n[Evaluating sigma-fitness] [Check this value is roughly the sum of the above values] (evaluate_fitness): "
        print str(chromosome_fitness_sum)

        #Finding the index of the maximal fitness value and using it to find the variable value that caused the fitness value.
        best_index = chromosome_fitnesses.index(max(chromosome_fitnesses))
        print "\n[Finding index of best fitness value] [Check the index is correct] (chromosome_fitnesses.index(max(chromosome_fitnesses))): "
        print str(best_index)
        best_value = chromosome_values[best_index]
        print "\n[Finding the best decimal value generated using the index] [Check against the value array to make sure this is the actual best value] (chromosome_values[best_index]): "
        print str(best_value)

        #Calculating the probabilities of the chromosomes.
        chromosome_probabilities = evaluate_probability(chromosome_fitnesses, chromosome_fitness_sum)
        print "\n[Calculating the probabilities of the chromosomes] [Check these values sum to approximately 1] (evaluate_probabilities): "
        print str(chromosome_probabilities)

        #Roulette ranking the chromosomes according to their probabilities.
        potential_parents = roulette_rank(chromosomes, chromosome_probabilities)
        print "\n[Ranking potential parents using the roulette system] [Check that the first member is the surviving best parent] (roulette_rank): "
        print str(potential_parents)

        #Performing crossover with the roulette ranked parents.
        children = crossover(potential_parents)
        print "\n[Performing crossover] [n/a] (crossover): "
        print str(children)
        
        #Mutating the children with a 50% mutation rate.
        mutated_children = mutate(50, children)
        print "\n[Mutating] [n/a] [Check that roughly half of the bits are flipping] (mutate): "
        print str(mutated_children)
        
        #Setting the mutated children as the original chromosomes for the next loop iteration.
        chromosomes = mutated_children
        print "\n[Setting the children as the new 'original' chromosomes for next iteration] [Compare with original chromosomes to make sure they are different] (assignment): "
        print str(chromosomes)
        print ""
        print ""
    print "\n----- END DEBUG -----"