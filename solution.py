import solution_test

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins. Twins are found in each kind of peer separately.
    # This is done by searching for and putting all two-digit box values in a list.
    # When a duplicate is encountered, that box and its value are added to a list of twins.

    row_twins = []
    row_twins_values = []
    for row in row_units:
        two_digit_values = []
        for box in row:
            if len(values[box]) == 2:
                if values[box] in two_digit_values:
                    if row not in row_twins:
                        row_twins.append(row)
                        row_twins_values.append(values[box])
                else:
                    two_digit_values.append(values[box])

    column_twins = []
    column_twins_values = []
    for column in column_units:
        two_digit_values = []
        for box in column:
            if len(values[box]) == 2:
                if values[box] in two_digit_values:
                    if column not in column_twins:
                        column_twins.append(column)
                        column_twins_values.append(values[box])
                else:
                    two_digit_values.append(values[box])

    square_twins = []
    square_twins_values = []
    for square in square_units:
        two_digit_values = []
        for box in square:
            if len(values[box]) == 2:
                if values[box] in two_digit_values:
                    if square not in square_twins:
                        square_twins.append(square)
                        square_twins_values.append(values[box])
                else:
                    two_digit_values.append(values[box])

    # Eliminate the naked twins as possibilities for their peers.
    # Look for all boxes that have a value with a digit included in a naked twin value for that peer,
    # and remove that digit form that box. Naked twins themselves are excluded from the elimination, of course.

    elimination_count = 0

    index = 0
    for row in row_twins:
        for box in row:
            for digit in row_twins_values[index]:
                if digit in values[box] and values[box] != row_twins_values[index]:
                    values[box] = values[box].replace(digit, '')
                    elimination_count += 1
        index += 1

    index = 0
    for column in column_twins:
        for box in column:
            for digit in column_twins_values[index]:
                if digit in values[box] and values[box] != column_twins_values[index]:
                    values[box] = values[box].replace(digit, '')
                    elimination_count += 1
        index += 1

    index = 0
    for square in square_twins:
        for box in square:
            for digit in square_twins_values[index]:
                if digit in values[box] and values[box] != square_twins_values[index]:
                    values[box] = values[box].replace(digit, '')
                    elimination_count += 1
        index += 1

    # The following condition is meant to cause constraint propagation to continue for new naked twins that are
    # revealed after the most recent round of twin identification and value elimination.
    # However, even though the resulting boards ARE in the possible solutions in solution_test.py
    # (the print statement below prints 'True' when the conditional statements aren't commented),
    # the unit tests do not pass. Therefore, this condition and its else are commented out.
    # if elimination_count == 0:
    print("Is board in solutions? " + str(values in solution_test.TestNakedTwins.possible_solutions_1
                                          or values in solution_test.TestNakedTwins.possible_solutions_2))
    return values
    # else:
       # naked_twins(values)

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units_1 = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']]
diagonal_units_2 = [['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
unitlist = row_units + column_units + square_units + diagonal_units_1 + diagonal_units_2
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
        Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
        If the sudoku is solved, return the sudoku.
        If after an iteration of both functions, the sudoku remains the same, return the sudoku.
        Input: A sudoku in dictionary form.
        Output: The resulting sudoku in dictionary form.
        """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)

    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
