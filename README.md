# GeneticAlgorithm
Genetic Algorithm that evaluates the best variables to use in order to maximise an objective function


Launch the program by navigating to the directory in a terminal window and typing:

python Main.py (command line arguments)


Required Command Line Arguments
-------------------------------

-l (integer) or --lowerval (integer)

Allows input of the lower bound for generated variables to be squeezed into.

-u (integer) or --upperval (integer)

Allows input of the upper bound for generated variables to be squeezed into.

-c (integer) or --cnums (integer)

Allows input of the desired number of chromosomes to be generated.


Optional Command Line Arguments
-------------------------------

-i (integer) or --iterations (integer)

Allows input of the desired number of iterations for the algorithm. If this command is not used, the program defaults to 1 iteration.

-m (interger) or --mutrate (integer)

Allows input of the desired mutation rate. If this command is not used, the program defaults to a 5% mutation rate.
