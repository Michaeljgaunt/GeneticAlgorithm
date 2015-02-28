import random
import GeneticAlgorithm

#Defining a debug version of the roulette rank function.
def roulette_rank(chrom_array, prob_array):
    print "\n[Ranking potential parents using the roulette system] [Check that the first member is the surviving best parent] (roulette_rank): "
    #Instantiating the total value.
    total = 0
    #Creating a new array to hold the chosen chromosomes.
    parent_array = []
    #Generating a random float between 0 and 1.
    random_num = random.random()
    #Iterating over the number of chromosomes.
    for i in xrange(0, len(chrom_array)):
        if (i != 0):
            print "\nGenerating random number: " + str(random_num)
        #If the parent array is not empty:
        if(parent_array):
            #Iterating over the number of chromosomes.
            for i in xrange(0, len(chrom_array)):
                #Adding the current iterating probability to the total.
                total += prob_array[i]
                print "Current total is: " + str(total)
                #If the total is greater than the random number:
                if (total >= random_num):
                    print "Total is now greater than the random number, appending chromosome at index " + str(i) + ": "
                    #Append the chosen chromosome in the parent array.
                    parent_array.append(chrom_array[i])
                    print str(chrom_array[i])
                    #Reset the total to 0.
                    total = 0
                    #Generating a new random number
                    random_num = random.random()
                    #Breaking into the outer for loop.
                    break
                print "total is less than random number, getting next chromosome."
        #If the parent array is empty:
        else:
            print "Adding surviving parent: "
            #Finding the index of the best chromosome.
            best_index = prob_array.index(max(prob_array))
            #Appending the best chromosome in the parent array to ensure its survival.
            parent_array.append(chrom_array[best_index])
            print str(chrom_array[best_index])
    print "\nRoulette ranking completed: "
    print str(parent_array)
    return parent_array

#Defining a debug version of the tournament_rank function.
def tournament_rank(chrom_array, prob_array, tourney_size):
    print "\n[Ranking potential parents using the tournament system] [Check that the best chromosome is winning the tournament] (roulette_rank): "
    #Saving the number of chromosomes.
    num_chroms = len(chrom_array)
    #Instantiating an array to hold the tournament selected chromosomes.
    tourney_array = []
    #instantiating an array to hold the selected parents.
    parent_array = []
    #Iterating over the number of chromosomes.
    for i in xrange(0, num_chroms):
        print "\nTournament number: " +str(i + 1)
        tourney_array = []
        #Iterating over the size of the tournament:
        for j in xrange(0, tourney_size):
            #Finding a random integer between 0 and 1 less than the chromosomal number inclusive.
            rand_int = random.randint(0, (num_chroms - 1))
            print "Generating random number: " + str(rand_int)
            #Using the random integer to index into the probability array.
            tourney_array.append(prob_array[rand_int])
            print "Adding chromosome probability to tournament: " + str(prob_array[rand_int])
        #Finding the tournament winner
        print "Full tournament is: "
        print str(tourney_array)
        tourney_winner = max(tourney_array)
        print "Tournament winner is: " + str(tourney_winner)
        #Finding the index of the winner in the probability array.
        winner_index = prob_array.index(tourney_winner)
        #Indexing into the chromosome array using the winner index.
        winner_chrom = chrom_array[winner_index]
        print "The winner corresponds to chromosome: " + str(chrom_array[winner_index])
        parent_array.append(winner_chrom)
    print "\nTournament ranking completed: "
    print str(parent_array)
    return parent_array

#Defining a debug version of the crossover function
def crossover(chrom_array, num_cuts):
    print "\n[Performing crossover] [Check the parents have been cut correctly] (crossover): "
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
        if(i == 1):    
            print "\nParent 1: " + str(chrom_a)
            print "Parent 2: " + str(chrom_b)
        print "\nThere will be " + str(num_cuts) + " cutting points."
        #Iterating for number of cut points
        for j in xrange(0, num_cuts):
            #Randomly generating a cut point.
            cut_point = random.randint(1, (chrom_len - 1))
            print "Cutting point " + str(j + 1) + " is at position " + str(cut_point) + ".\n"
            recombined = recombination(chrom_a, chrom_b, cut_point)
            child_a = recombined.get("child_a")
            child_b = recombined.get("child_b")
            print "Child 1 is: " + str(child_a)
            print "Child 2 is: " + str(child_b) + "\n"

            chrom_a = child_a
            chrom_b = child_b
        #Appending the two child chromosomes in the child array.
        child_array.append(chrom_a)
        child_array.append(chrom_b)
    #Returning the child chromosomes.
    print "Crossover completed: "
    print str(child_array)
    return child_array  

#Defining a debug version of the recombination function.
def recombination(chrom_a, chrom_b, cut_point):
    #Cutting both chromosomes and combining the segments (one from each parent). Saving as a new chromosome.
    child_a = list(chrom_a[0:cut_point]) + list(chrom_b[cut_point:])
    child_b = list(chrom_b[0:cut_point]) + list(chrom_a[cut_point:])
    print "Child 1 will consist of: "
    print "Parent 1, fragment 1: " + str(list(chrom_a[0:cut_point]))
    print "and parent 2, fragment 2: " + str(list(chrom_b[cut_point:]))
    print "Child 2 will consist of: "
    print "Parent 2, fragment 1: " + str(list(chrom_b[0:cut_point]))
    print "and parent 1, fragment 2: " + str(list(chrom_a[cut_point:]))
    #Returning children in a dicitonary.
    return {"child_a":child_a, "child_b":child_b}      

#Defining a debug version of the mutate function.
def mutate(mutation_rate, chrom_array):
    print "\n[Mutating] [Check that bits are flipping correctly] (mutate): "
    #Saving the number of chromosomes.
    num_chroms = len(chrom_array)
    #Saving the length of chromosomes.
    chrom_len = len(chrom_array[0])
    #Iterating over the number of chromosomes.
    for i in xrange(0, num_chroms):
        #Iterating over each chromosome bit
        for j in xrange(0, chrom_len):
            #If mutation rate was entered as 0, the mutator is set as 0.
            if(mutation_rate == 0):
                random_num = 0
            #If mutation rate is higher than 0:
            else:
                #Generates a random number between 1 and 100.
                random_num = random.randint(0, 100)
            #If the random number is less than or equal to the given mutation rate.
            if (random_num <= mutation_rate):
                print "Chromosome number " + str(i + 1) + ", bit number " + str(j + 1) + " has mutated to " + str(1 - chrom_array[i][j]) + "."
                #The bit at the current position is flipped.
                chrom_array[i][j] = (1 - chrom_array[i][j])
    print list(chrom_array)
    return list(chrom_array)

#Defining a function to launch a debug of the genetic algorithm.
def debug(args):
    print "\n----------------------------------- DEBUG MODE ---------------------------------------"
    print "Generating " + str(args.cnum) + " chromosomes."                                     
    print "Squeezing with a range of " + str(args.lowerval) + " - " + str(args.upperval) + ""
    print "Iterating " + str(args.iterations) + " times."
    print "Mutation rate is " + str(args.mutrate) + "%."
    if(args.rouletterank):
        print "Chromosomes will be ranked by the roulette method\n"
    if(args.tournamentrank):
        print "Chromosomes will be ranked by the tournament method (size " + str(args.tournamentrank) + ")\n"
    print "The debug statements are printed in the order that the functions are"
    print "called in __main__\n"
    print "Layout:"
    print "[Description of event] [Possible errors to check] (corresponding function name):"
    print "[values returned by function]"
    print "--------------------------------------------------------------------------------------\n"
    
    #Generating chromosomes.
    chromosomes = GeneticAlgorithm.GA.generate_chromosomes(args.upperval, args.cnum)
    print "\n[Randomly generating first set of chromosomes] [Check that there are " + str(args.cnum) + " chromosomes] (generate_chromosomes): "
    print str(chromosomes) 
    print ""
    print ""
    
    #Iterating the algorithm 5 times.
    for i in xrange(0, args.iterations):
        print "\nBeginning iteration " + str(i + 1) + "."

        #Calculating the decimal values of the bit string chromosomes, squeezing in a range of 2-60.
        chromosome_values = GeneticAlgorithm.GA.convert_bitstring(chromosomes, args.lowerval, args.upperval)
        print "\n[Converting to decimals] [Check the values are squeezed within the bounds] (convert_bitstring): " 
        print str(chromosome_values)
        #Evaluating the chromosomes' fitness and summing their values.
        chromosome_evaluation = GeneticAlgorithm.GA.evaluate_fitness(chromosome_values)
        chromosome_fitnesses = chromosome_evaluation.get("fitnesses")
        print "\n[Evaluating fitnesses] [n/a] (evaluate_fitness): "
        print str(chromosome_fitnesses)
        
        #Checking to see if a fitness threshold has been provided.
        if(args.fitnessthreshold):
            #Checking to see if any of the fitnesses of the generated chromosmoes have reached the threshold.
                if(max(chromosome_fitnesses) >= args.fitnessthreshold):
                    print "A chromosomes has exceeded the fitness threshold of " + str(args.fitnessthreshold) + ", mutation rate has been reduced to 1%"
                    #If they have, the mutation rate is set to 1.
                    args.mutrate = 1
                    
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
        chromosome_probabilities = GeneticAlgorithm.GA.evaluate_probability(chromosome_fitnesses, chromosome_fitness_sum)
        print "\n[Calculating the probabilities of the chromosomes] [Check these values sum to approximately 1] (evaluate_probabilities): "
        print str(chromosome_probabilities)

        #Ranking the chromosomes according to their probabilities.
        if(args.rouletterank):
            potential_parents = roulette_rank(chromosomes, chromosome_probabilities)
        if(args.tournamentrank):
            potential_parents = tournament_rank(chromosomes, chromosome_probabilities, args.tournamentrank)

        #Performing crossover with the roulette ranked parents.
        children = crossover(potential_parents, 2)
        
        #Mutating the children.
        mutated_children = mutate(args.mutrate, children)
        
        #Setting the mutated children as the original chromosomes for the next loop iteration.
        chromosomes = mutated_children
        print "\n[Setting the children as the new 'original' chromosomes for next iteration] [Compare with original chromosomes to make sure they are different] (assignment): "
        print str(chromosomes)
        print ""
        print ""
    print "\n----- END DEBUG -----\n"