# GeneticAlgorithm
Genetic Algorithm that evaluates the best variables to use in order to maximise an objective function.
User can input integers for the required range of variables , desired number of iterations, desired number
of chromosomes and desired mutation rate.


Launch the program with default values by navigating to the directory in a terminal window and typing:

python Main.py

The default values are as follows: 
range 0 - 100,
1 iteration,
10 chromosomes,
5% mutation rate.

Required Command line Arguments
---------------------------------



-rr

--rouletterank


Set the chromosomal ranking method to roulette.


-tr (integer)

--tournamentrank (integer)


Set the chromosomal ranking method to tournament of size (integer).




Optional Command Line Arguments
-----------------------



-l (integer)

--lowerval (integer)


Input an integer for the range's lower bound.


-u (integer)

--upperval (integer)


Input an integer for the range's upper bound.



-c (integer)

--cnums (integer)


Input an integer for the desired number of chromosomes.



-i (integer)

--iterations (integer)


Input an integer for the desired number of iterations.



-m (interger)

--mutrate (integer)


Input an integer between 1 and 100 for the desired mutation rate.



-d

--debug


Enter debug mode.



-p

--plot


Plot the results of the genetic algorithm on a graph.



