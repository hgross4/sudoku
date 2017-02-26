# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Because of the rules of Sudoku, digits in the values of naked twins cannot be the solution for other peers of those twins, i.e., those boxes are constrained not to have those digits as their solution. When those digits are removed as possible solutions for those boxes, only_choice, elimination, and possibly other constraints may be revealed, as well as other naked twins, which may further constrain the values of other peers. The general approach, then, is to enforce the constraint, check the results, and continue thusly, thus propagating the constraints to reduce the possible solutions as much as possible.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The board diagonals are added to the list of peers that are constrained in the same was as other peers: no duplicate values in each diagonal. Eliminate and reduce are used to whittle down the possible values for each box in each diagonal. Doing so tends to introduce other contsraints in other peer sets that can be used to further solve the board.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
