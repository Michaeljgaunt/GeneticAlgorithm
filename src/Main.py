
import argparse
import GeneticAlgorithm

#Main method.
if __name__ == "__main__":
    
    #Adding an ArgumentParser to set up command line commands.
    parser = argparse.ArgumentParser(description="Genetic algorithm to evaluate the best variables to maximise an objective function", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    #Adding commands.
    parser.add_argument("-i", "--iterations", help="Enter the command followed by an integer number to represent the number of desired iterations of the genetic algorithm.", default='5', type=int)
    parser.add_argument("-l", "--lowerval", help="Enter the minimum value for the variable.", default='0', type=int)
    parser.add_argument("-u", "--upperval", help="Enter the maximum value for the variable.", default='100', type=int)
    parser.add_argument("-c", "--cnum", help="Enter a value for the desired number of chromosomes.",  default='10', type=int)
    parser.add_argument("-m", "--mutrate", help="Enter a value for the desired mutation rate (integer from 1 - 100).", default='5', type=int, choices=range(1, 101), metavar="")
    parser.add_argument("-d", "--debug", help="Debug mode.", action='store_true')

    #Parsing the command line arguments.
    args = parser.parse_args()
    
    if(args.debug):
        GeneticAlgorithm.Debug.debug()
    else:
        print "\nThe algorithm will iterate " + str(args.iterations) + " time(s)."
        print str(args.cnum ) + " chromosomes will be randomly generated. "
        print "Generated variables will be squeezed into the range: " + str(args.lowerval) + " - " + str(args.upperval) + "."
        print "Following each iteration, a mutation rate of " + str(args.mutrate) + "% will be applied."
        print "\nGenerating chromosomes..."
        #Randomly generating n chromosomes (n provided in command line arguments). Length of the chromosome is determined by the upper bound given in the command line arguments.
        chromosomes = GeneticAlgorithm.GA.generate_chromosomes(args.upperval, args.cnum)

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

            #Calculating the probabilities of the chromosomes.
            chromosome_probabilities = GeneticAlgorithm.GA.evaluate_probability(chromosome_fitnesses, chromosome_fitness_sum)

            #Roulette ranking the chromosomes according to their probabilities.
            print "Ranking potential parents..."
            potential_parents = GeneticAlgorithm.GA.roulette_rank(chromosomes, chromosome_probabilities)

            #Performing crossover with the roulette ranked parents.
            print "Performing crossover and mutation..."
            children = GeneticAlgorithm.GA.crossover(potential_parents)

            #Mutating the children by the mutation rate given in the command line arguments.
            mutated_children = GeneticAlgorithm.GA.mutate(args.mutrate, children)

            #Setting the mutated children as the original chromosomes for the next loop iteration.
            chromosomes = mutated_children

            #Printing the value found that maximises the objecive function.
            print "Iteration " + str(i + 1) + " finished. Best value found is " + str(best_value) + ".\n"