
import math
import numpy
import random
import matplotlib.pyplot as graph

class GA:
    
    #Instantiating a class variable to hold the best value generated.
    best_value = 0
    
    #Defining the objective function.
    @staticmethod
    def objective_function(x):
        result = (x * (math.sin(x) * (math.pi * 10)))
        #result = x * x * x
        return result

    #Defining a function to randomly generate chromosomes.
    @staticmethod
    def generate_chromosomes(upper_bound, chrom_num):
        #Finding the minimum bit string length needed to hold the upper bound integer.
        bs_length = int(math.ceil(math.log(upper_bound, 2)))
        #Instantiating a list to hold the chromosomes.
        chrom_array = numpy.zeros((chrom_num, bs_length))
        #Iterating up to the number of chromosomes wanted.
        for i in xrange(0, (chrom_num)):
            #Iterating over each bit in the bit string
            for j in xrange(0, (bs_length - 1)):
                #Finding a random integer between 1 and 10 inclusive.
                rand_int = random.randint(1, 10)
                #If the integer is <= 4, the bit in question is assigned a 0.
                if(rand_int <= 5):
                    chrom_array[i][j] = 0
                #If the integer is >= 5, the bit in question is assigned a 1.                
                else:
                    chrom_array[i][j] = 1
        #The randomised chromosomes are returned in a list.
        return list(chrom_array)

    #Defining a function to convert a bit string into a decimal value.
    @staticmethod
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
    @staticmethod    
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
            fitness = GA.objective_function(x)
            #Saving the fitness value in an array.
            fitness_array[i] = fitness
            #Adding it to the sum value.
            sum += fitness
        #Returning the fitness array and the sum.
        return {"fitnesses":list(fitness_array), "sum":sum}

    #Defining a funtion to evaluate the probability of a given variable.
    @staticmethod
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

    #Defining a function to rank the chromosomes based on the roulette method.
    @staticmethod
    def roulette_rank(chrom_array, prob_array):
        #Instantiating the total value.
        total = 0
        #Saving the number of chromosomes.
        num_chroms = len(chrom_array)
        #Creating a new array to hold the chosen chromosomes.
        parent_array = []
        #Generating a random float between 0 and 1.
        random_num = random.random()
        #Iterating over the number of chromosomes.
        for i in xrange(0, num_chroms):
            #If the parent array is not empty:
            if(parent_array):
                #Iterating over the number of chromosomes.
                for i in xrange(0, num_chroms):
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

    #Defining a function to rank the chromosomes based on the k-tournament method.
    @staticmethod
    def tournament_rank(chrom_array, prob_array, tourney_size):
        #Saving the number of chromosomes.
        num_chroms = len(chrom_array)
        #Instantiating an array to hold the tournament selected chromosomes.
        tourney_array = []
        #instantiating an array to hold the selected parents.
        parent_array = []
        #Iterating over the number of chromosomes.
        for i in xrange(0, num_chroms):
            tourney_array = []
            #Iterating over the size of the tournament:
            for j in xrange(0, tourney_size):
                #Finding a random integer between 0 and 1 less than the chromosomal number inclusive.
                rand_int = random.randint(0, (num_chroms - 1))
                #Using the random integer to index into the probability array.
                tourney_array.append(prob_array[rand_int])
            #Finding the tournament winner
            tourney_winner = max(tourney_array)
            #Finding the index of the winner in the probability array.
            winner_index = prob_array.index(tourney_winner)
            #Indexing into the chromosome array using the winner index.
            winner_chrom = chrom_array[winner_index]
            parent_array.append(winner_chrom)
        return parent_array

    #Defining a function to perform crossover of chromosomes.
    @staticmethod
    def crossover(chrom_array, num_cuts):
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
            #Iterating for number of cut points
            for i in xrange(0, num_cuts):
                #Randomly generating a cut point.
                cut_point = random.randint(1, (chrom_len - 1))
                recombined = GA.recombination(chrom_a, chrom_b, cut_point)
                child_a = recombined.get("child_a")
                child_b = recombined.get("child_a")
                chrom_a = child_a
                chrom_b = child_b
            #Appending the two child chromosomes in the child array.
            child_array.append(chrom_a)
            child_array.append(chrom_b)
        #Returning the child chromosomes.
        return child_array

    #Defining a function to cut two chromosomes and recombine them.
    @staticmethod
    def recombination(chrom_a, chrom_b, cut_point):
        #Cutting both chromosomes and combining the segments (one from each parent). Saving as a new chromosome.
        child_a = list(chrom_a[0:cut_point]) + list(chrom_b[cut_point:])
        child_b = list(chrom_b[0:cut_point]) + list(chrom_a[cut_point:])
        #Returning children in a dicitonary.
        return {"child_a":child_a, "child_b":child_b}

    #Defining a function to randomly mutate bit values in a chromosome according to a given mutation rate.
    @staticmethod
    def mutate(mutation_rate, chrom_array):
        #Saving the number of chromosomes.
        num_chroms = len(chrom_array)
        #Saving the length of chromosomes.
        chrom_len = len(chrom_array[0])
        #Iterating over the number of chromosomes.
        for i in xrange(0, num_chroms):
            #If mutation rate was entered as 0, the mutator is set as 0.
            if(mutation_rate == 0):
                break
            #Iterating over each chromosome bit
            for j in xrange(0, chrom_len):
                #Generates a random number between 1 and 100.
                random_num = random.randint(0, 100)
                #If the random number is less than or equal to the given mutation rate.
                if (random_num <= mutation_rate):
                    #The bit at the current position is flipped.
                    chrom_array[i][j] = (1 - chrom_array[i][j])
        return list(chrom_array)
    
    #Defining a method to print the results on a graph.
    @staticmethod
    def graph_results(xaxis, yaxis, yaxis2, title, xlabel, ylabel):
        #Plotting datasets onto the x-axis and y-axis.
        line1 = graph.plot(xaxis, yaxis)
        line2 = graph.plot(xaxis, yaxis2)
        graph.axis([min(xaxis), max(xaxis), (min(yaxis) * 0.95), (max(yaxis2) * 1.05)])
        graph.setp(line1, color="r")
        graph.setp(line2, color="b")
        graph.title(title)
        graph.xlabel(xlabel)
        graph.ylabel(ylabel)
        graph.show()
    