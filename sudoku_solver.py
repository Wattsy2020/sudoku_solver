def input_grid():
    print('\nEnter the sudoku row by row with 0 representing an empty space')
    print('e.g. a row could look like 0 0 1 0 4 0 6 0 9')

    grid = []
    i = 1
    while i < 10:
        row = input('Enter row {}: '.format(i))
        squares = list(row.replace(' ', ''))

        if len(squares) != 9:
            print('Please enter 9 numbers')
            continue

        # convert chars to int
        try:
            squares = [int(x) for x in squares]
        except ValueError:
            print('Please enter numbers not letters')
            continue

        grid.append(squares)
        i += 1

    print('The grid is:\n')
    print_grid(grid)
    correct = input('\nDo you want to re-enter the grid? [y/n]: ').lower()
    if correct == 'y':
        grid = input_grid()

    return grid


def print_grid(grid):
    for row in grid:
        print('  ', end='')
        for square in row:
            print(square, end='  ')
        print()


def get_section_number(row, column):
    row -= row % 3
    column -= column % 3
    return int(row + column/3)


def initialise_resources(grid):
    # initialise the hash sets and empty spaces
    spaces = []
    for i in range(9):
        for j in range(9):
            square = grid[i][j]
            if square == 0:
                spaces.append([i, j])
            else:
                row_sets[i].add(square)
                column_sets[j].add(square)
                section_sets[get_section_number(i, j)].add(square)

    return spaces


def find_solution(grid, spaces):
    if len(spaces) == 0: return grid  # if there are no empty spaces we are done

    # initialise useful variables
    row = spaces[0][0]
    column = spaces[0][1]
    section = get_section_number(row, column)
    avoid_set = set(row_sets[row].union(column_sets[column]).union(section_sets[section]))

    # try to fill the first empty space
    for i in range(1, 10):
        if i not in avoid_set:
            # update grid and avoid sets
            grid[row][column] = i
            row_sets[row].add(i)
            column_sets[column].add(i)
            section_sets[section].add(i)

            # fill the rest of the spaces recursively
            solution = find_solution(grid, spaces[1:])
            if solution: return solution

            grid[row][column] = 0
            row_sets[row].remove(i)
            column_sets[column].remove(i)
            section_sets[section].remove(i)

    return  # there is no solution in this branch


def main():
    grid = input_grid()
    
    spaces = initialise_resources(grid)

    solved_grid = find_solution(grid, spaces)

    if not solved_grid:
        print('Invalid grid entered, there is no solution')
    else:
        print('Solution:\n')
        print_grid(solved_grid)


row_sets = [set() for i in range(9)]
column_sets = [set() for j in range(9)]
section_sets = [set() for k in range(9)]

if __name__ == '__main__':
    main()
