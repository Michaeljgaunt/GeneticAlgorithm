
import GeneticAlgorithm
import argparse

if __name__ == "__main__":
    
    #Adding an ArgumentParser to set up command line commands.
    parser = argparse.ArgumentParser(description='Genetic algorithm to evaluate the best variables to maximise an objective function')
    #Adding commands.
    parser.add_argument("-i", "--iterations", help="Enter the command followed by an integer number to represent the number of desired iterations of the genetic algorithm. If this command isn't entered manually, the program runs 1 iteration by default.", default='1', type=int)
    parser.add_argument("-u", "--upperval", help="Enter the maximum value for the variable.", required=True, type=int)
    parser.add_argument("-l", "--lowerval", help="Enter the maximum value for the variable.", required=True, type=int)
    parser.add_argument("-c", "--cnum", help="Enter a value for the desired number of chromosomes.", required=True, type=int)
    parser.add_argument("-m", "--mutrate", help="Enter a value for the desired mutation rate (integer from 1 - 100). If this command isn't entered manually, the program uses a mutation rate of 5%", default='5', type=int, choices=range(0, 100))
    #Parsing the command line arguments.
    args = parser.parse_args()
    
    #Generating an array of chromosomes based on the command line input.
    print "\nRandomly generating " + str(args.cnum) + " chromosomes for generation 1..."
    chromosomes = GeneticAlgorithm.generate_chromosomes(args.upperval, args.cnum)
    #Converting the chromosomal bit strings into integer values.
    bitstring_values = GeneticAlgorithm.convert_bitstring(chromosomes, args.lowerval, args.upperval)
    #Evaluating the chromosomes fitnesses and summing them.
    print "Evaluating chromosomes..."
    evaluated_chromosomes = GeneticAlgorithm.evaluate_fitness(bitstring_values)
    fitnesses = list(evaluated_chromosomes.get("fitnesses"))
    sum = evaluated_chromosomes.get("sum") 
    print "Generation 1 has sigma-fitness: " + str(sum)
    #Calculating the probabilities using the chromosomes.
    probabilities = GeneticAlgorithm.evaluate_probability(fitnesses, sum)
    #Finding the index of the best fitness value.
    best_index = fitnesses.index(max(fitnesses))
    #Finding the best value in the generation.
    best_value = bitstring_values[best_index]
    print "After generation 1, the best value found for the objective function is: " + str(best_value)
    
    #Iterating up to the number of iterations entered on the command line.
    for i in xrange(0, (args.iterations-1)):
        print "\nCrossing over chromosomes to produce generation " + str(i + 2) + "..."
        #Calling a function to roulette rank the chromosomes.
        roulette_ranked_chromosomes = GeneticAlgorithm.roulette_rank(chromosomes, probabilities)
        #Calling a function to perform crossover on the chromosomes.
        child_chroms = roulette_ranked_chromosomes  #GeneticAlgorithm.crossover(roulette_ranked_chromosomes) 
        #Mutating the new children chromosomes.
        print "Mutating generation " + str(i + 2) + "..."
        mutated_child_chroms = GeneticAlgorithm.mutate(args.mutrate, child_chroms)
        #Converting the child bit strings into integer values.
        child_bitstring_values = GeneticAlgorithm.convert_bitstring(mutated_child_chroms, args.lowerval, args.upperval)
        #Evaluating the child chromosomes fitnesses and summing them.
        print "Evaluating generation " + str(i + 2) + "..."
        child_evaluated_chromosomes = GeneticAlgorithm.evaluate_fitness(child_bitstring_values)
        child_fitnesses = list(child_evaluated_chromosomes.get("fitnesses"))
        child_sum = child_evaluated_chromosomes.get("sum")
        print "Generation " + str(i + 2) + " has sigma-fitness: " + str(child_sum)
        #Calculating the child chromosomes probabilities.
        child_probabilities = GeneticAlgorithm.evaluate_probability(child_fitnesses, child_sum)
        chromosomes = child_chroms[:]
        probabilities = child_probabilities[:]
        #Finding the index of the best fitness value.
        best_index = child_fitnesses.index(max(child_fitnesses))
        #Finding the best value in the generation.
        best_value = child_bitstring_values[best_index]
        print "After generation " + str(i + 2) + ", the best value found for the objective function is: " + str(best_value)
