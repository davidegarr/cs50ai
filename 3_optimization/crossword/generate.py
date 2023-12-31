import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
            constraints; in this case, the length of the word.)
        """
        
        for var in self.domains.copy():
            for word in self.domains[var].copy():
                if len(word) != int(var.length):
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        if self.crossword.overlaps[x, y] != None:
            overlap_1, overlap_2 = self.crossword.overlaps[x, y]

            to_remove = set()  # collect words to remove
            for word_x in self.domains[x]:
                # Check if there is no word_y such that word_x and word_y overlap
                if not any(word_x[overlap_1] == word_y[overlap_2] for word_y in self.domains[y]):
                    to_remove.add(word_x)

            for word in to_remove:  # Remove words after iterating
                self.domains[x].remove(word)
                revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        in_queue = []
        for var1 in self.domains:
            for var2 in self.domains:
                if var1 != var2:
                    new_arc = (var1, var2)
                    in_queue.append(new_arc)
        while in_queue:
            x = in_queue[0][0]
            y = in_queue[0][1]
            in_queue.remove(in_queue[0])
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                neighbors = self.crossword.neighbors(x)
                for z in neighbors:
                    in_queue.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if all(variable in assignment for variable in self.crossword.variables):
            return True
        return False


    def consistent(self, assignment):
        # Check for duplicate assignments
        if len(assignment) != len(set(assignment.values())):
            return False

        # Check for conflicts between neighboring values
        checked_pairs = set()
        for var in assignment:
            for neighbor in self.crossword.neighbors(var):
                pair = frozenset((var, neighbor))
                if pair in checked_pairs or neighbor not in assignment:
                    continue
                overlap = self.crossword.overlaps.get((var, neighbor))
                if overlap and assignment[var][overlap[0]] != assignment[neighbor][overlap[1]]:
                    return False
                checked_pairs.add(pair)

        return True



    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        #get all the neighbors not assigned
        unassigned_neighbors = [v for v in self.crossword.neighbors(var) if v not in assignment]

        #maps var to number of values ruled out
        impact = {}

        #Create a temporary assignment, setting `var` to the potential value, 
        #and then iteratively evaluating how this choice affects the possible 
        #assignments to its unassigned neighbors. The `count` variable tracks the 
        #number of times the chosen value for `var` leads to inconsistent assignments 
        #for the neighbors.
        for value in self.domains[var]:
            count = 0
            temp_assignment = assignment.copy()
            temp_assignment[var] = value
            for neighbor in unassigned_neighbors:
                for neighbor_val in self.domains[neighbor]:
                    temp_assignment[neighbor] = neighbor_val
                    if not self.consistent(temp_assignment):
                        count += 1
            impact[value] = count

        #orders value in asc order of impact      
        ordered_values = sorted(self.domains[var], key=lambda x: impacts[x])

        return ordered_values



    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_variable = None
        unassigned_variable_length = float('inf')
        num_neighbors = 0
        for var in self.domains:
            if var not in assignment:
                if len(self.domains[var]) < unassigned_variable_length:
                    unassigned_variable = var
                    unassigned_variable_length = len(self.domains[var])
                    num_neighbors = len(self.crossword.neighbors(var))
                elif len(self.domains[var]) == unassigned_variable_length and len(self.crossword.neighbors(var)) > num_neighbors:
                    unassigned_variable = var
                    unassigned_variable_length = len(self.domains[var])
                    num_neighbors = len(self.crossword.neighbors(var))

        return unassigned_variable

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            #print("assignment complete: ", assignment)
            return assignment
        #print("assignment not complete. Current assignement in backtrack:", assignment)
        var = self.select_unassigned_variable(assignment)
        #print("var = self.select_unassigned_variable(assignment) = ", var)
        for word in self.domains[var]:
            assignment[var] = word
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result:
                    return result
            del assignment[var]
        #print(f"final assignment before failure: {assignment}")
        return None
                    


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
