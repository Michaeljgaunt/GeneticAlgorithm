
import argparse
import sys
import GeneticAlgorithm    
import Debug
    
#Main method.
if __name__ == "__main__":

    #Adding an ArgumentParser to set up command line commands.
    parser = argparse.ArgumentParser(description="Genetic algorithm to evaluate the best variables to maximise an objective function", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    #Adding commands.
    parser.add_argument("-i", "--iterations", help="Enter the command followed by an integer number to represent the number of desired iterations of the genetic algorithm.", default='3', type=int)
    parser.add_argument("-l", "--lowerval", help="Enter the minimum value for the variable.", default='0', type=int)
    parser.add_argument("-u", "--upperval", help="Enter the maximum value for the variable.", default='31', type=int)
    parser.add_argument("-c", "--cnum", help="Enter an even integer value for the desired number of chromosomes.",  default='4', type=int)
    parser.add_argument("-m", "--mutrate", help="Enter a value for the desired mutation rate (integer from 0 - 100).", default='5', type=int, choices=range(0, 101), metavar="")
    parser.add_argument("-s", "--slicepoints", help="Enter the number of slice points to use during crossover.", default='1', type=int)
    optfunc = parser.add_mutually_exclusive_group()
    optfunc.add_argument("-d", "--debug", help="Debug mode.", action='store_true')
    optfunc.add_argument("-p", "--plot", help="Plot a graph of the results.", action='store_true')
    rank = parser.add_mutually_exclusive_group(required=True)
    rank.add_argument("-rr", "--rouletterank", help="Rank potential parent chromosomes based on the roulette method.", action='store_true')
    rank.add_argument("-tr", "--tournamentrank", help="Rank potential parent chromosomes based on the tournament method.", type=int)



    #Parsing the command line arguments.
    args = parser.parse_args()

    #Checking to see if the command line input for number of chromosomes is an even number.
    if(args.cnum % 2 != 0):
        #If it's not, print a statement to the console and exit the program.
        print "The number of desired chromosomes must be even for crossover to work."
        sys.exit(1)

    #If debug mode is engaged:
    if(args.debug):
        #The debug function is called.
        Debug.debug(args)
    #If not, the program carries on as usual.
    else:
        print "\nThe algorithm will iterate " + str(args.iterations) + " time(s)."
        print str(args.cnum ) + " chromosomes will be randomly generated. "
        print "Generated variables will be squeezed into the range: " + str(args.lowerval) + " - " + str(args.upperval) + "."
        if(args.rouletterank):
            print "The chromosomes will be ranked according to the roulette method."
        if(args.tournamentrank):
            print "The chromosomes will be ranked according to the tournament method (tournament size is set as " + str(args.tournamentrank) + ")."
        print str(args.slicepoints) + " slice point(s) will be used during crossover."
        print "Following each iteration, a mutation rate of " + str(args.mutrate) + "% will be applied."
        print "\nGenerating chromosomes...\n"
        #Randomly generating n chromosomes (n provided in command line arguments). Length of the chromosome is determined by the upper bound given in the command line arguments.
        chromosomes = GeneticAlgorithm.GA.generate_chromosomes(args.upperval, args.cnum)        
        #If plot mode is engaged:
        if(args.plot):
            #Two arrays are instantiated to hold x-values and y-values.
            x_array = []
            y_array = []
            global_y_array = []
        

        #Iterating the algorithm n times (n provided in command line arguments).
        for i in xrange(0, args.iterations):

            #Calculating the decimal values of the bit string chromosomes. Passing in the range from the command line arguments to squeeze the values.
            chromosome_values = GeneticAlgorithm.GA.convert_bitstring(chromosomes, args.lowerval, args.upperval)

            #Evaluating the chromosomes' fitness and summing their values.
            print "Evaluating chromosomes..."
            chromosome_evaluation = GeneticAlgorithm.GA.evaluate_fitness(chromosome_values)
            chromosome_fitnesses = chromosome_evaluation.get("fitnesses")
            chromosome_fitness_sum = chromosome_evaluation.get("sum")

            #Finding the index of the maximal fitness value and using it to find the variable value that caused the fitness value.
            best_index = chromosome_fitnesses.index(max(chromosome_fitnesses))
            best_value = chromosome_values[best_index]

            #If it is the first iteration:
            if(i == 0):
                #The global best value is set as the current best value.
                GeneticAlgorithm.GA.best_value = best_value
            #If it is any other iteration:
            else:
                #A check is done to see if the current best value is better than the global best value.
                if(best_value > GeneticAlgorithm.GA.best_value):
                    #If it is, the current best value becomes the new global best value.
                    GeneticAlgorithm.GA.best_value = best_value
           #If plot mode is engaged:
            if(args.plot):
                #Iteration number and best value are saved in the plot arrays.
                x_array.append(i)
                y_array.append(best_value)   
                global_y_array.append(GeneticAlgorithm.GA.best_value)  

            #Calculating the probabilities of the chromosomes.
            chromosome_probabilities = GeneticAlgorithm.GA.evaluate_probability(chromosome_fitnesses, chromosome_fitness_sum)

            #Ranking the potential parent chromosomes.
            print "Ranking potential parents..."
            #By roulette method. 
            if(args.rouletterank):
                potential_parents = GeneticAlgorithm.GA.roulette_rank(chromosomes, chromosome_probabilities)
            #By tournament method.
            if(args.tournamentrank):
                potential_parents = GeneticAlgorithm.GA.tournament_rank(chromosomes, chromosome_probabilities, args.tournamentrank)

            #Performing crossover with the roulette ranked parents.
            print "Performing crossover and mutation..."
            children = GeneticAlgorithm.GA.crossover(potential_parents, 2)

            #Mutating the children by the mutation rate given in the command line arguments.
            mutated_children = GeneticAlgorithm.GA.mutate(args.mutrate, children)

            #Setting the mutated children as the original chromosomes for the next loop iteration.
            chromosomes = mutated_children

            #Printing the value found that maximises the objecive function.
            print "Iteration " + str(i + 1) + " finished. Best value found is " + str(best_value) + ".\n"
        print "Finished all " + str(args.iterations) + " iterations. The overall best value found is " + str(GeneticAlgorithm.GA.best_value) + ".\n"
        if (args.plot):
            GeneticAlgorithm.GA.graph_results(x_array, y_array, global_y_array, "A Graph Showing The Best Generated Value For Each Iteration", "Iteration Number", "Best Generated Value")
