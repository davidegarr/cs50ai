# Problem Set 30: Crossword
In this project, I worked ont the world of Constraint Satisfaction Problems (CSPs) by creating a crossword puzzle solver. The objective was to fill in words into a crossword puzzle grid such that all the constraints of the puzzle are satisfied.

By leveraging the following techniques, the crossword solver intelligently navigates the problem space, and fills in the crossword grid while respecting constraints, and efficiently finds a solution:

### Backtracking Search:
In the crossword problem, backtracking involves attempting to fit a word into a specific slot on the grid. If a word doesn’t fit because it violates a constraint, such as mismatched letters with adjacent words, the algorithm backtracks and tries a different word until a suitable one is found or it determines that no word fits.

### Forward Checking:
After placing a word in a slot, forward checking anticipates issues with neighboring, intersecting slots. For example, if "Atom" is placed in a vertical slot, a neighboring horizontal slot might intersect at the letter "A". Forward checking will then ensure that only words starting or containing the letter "A" are considered for that neighboring slot.

### Constraint Propagation:
*Node Consistency*: In the case of a crossword puzzle, this means making sure that every value in a variable's domain has the same number of letters as the variable's length.

*Arc Consistency*: In the crossword, every intersecting point between two word slots is an arc. The AC-3 algorithm checks and removes word choices. If a word is chosen for one slot, the choices for an intersecting slot are reduced to words that have the appropriate letter at the intersection.

### Heuristics
When deciding which slot to fill next, MRV can be used. Slots that have the fewest valid word choices (due to intersecting constraints from already filled slots) are chosen first. This strategy narrows down possibilities and increases the likelihood of a quick solution.

For a given slot, words are ordered based on the LCV heuristic. The idea is to choose the word that imposes the least constraint on the neighboring slots. For instance, if one word results in more possible valid words for neighboring slots than another word, the first word is selected.

I implemented enforce_node_consistency, revise, ac3, assignment_complete, consistent, order_domain_values, selected_unassigned_variable, and backtrack in generate.py.