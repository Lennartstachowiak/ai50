import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        """ Changed """
        """ Maybe we have to create an own list for all known mines """
        if len(self.cells) == self.count:
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        """ Maybe we have to create a list for all known safes """
        if self.count <= 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        for element in self.cells:
            if element == cell:
                self.cells.remove(element)
                self.count -= 1
                # existing_mines = self.known_mines()
                # if cell not in existing_mines:
                #     Sentence(cell, 1)
                break

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        for element in self.cells:
            if element == cell:
                self.cells.remove(element)
                # existing_safes = self.known_safes()
                # if cell not in existing_safes:
                #     Sentence(cell, 0)
                break


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
        """
        self.moves_made.add(cell)
        """
            2) mark the cell as safe
        """
        self.mark_safe(cell)
        # changes all sentences in knowledge
        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.mark_safe(cell)
        """
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
        """
        cells_around = set()
        for i in range(cell[0]-1, cell[0]+2):
            for j in range(cell[1]-1, cell[1]+2):
                if (i, j) == cell:
                    continue
                if (i, j) in self.safes or (i, j) in self.moves_made:
                    continue
                if (i, j) in self.mines:
                    count -= 1
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    cells_around.add((i, j))
        if len(cells_around) > 0 or count > 0:
            new_sentence = Sentence(cells_around, count)
            if new_sentence not in self.knowledge:
                self.knowledge.append(new_sentence)
        """
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
        """
        for sentence in self.knowledge:
            if sentence.known_mines():
                for mine in set(sentence.known_mines()):
                    self.mines.add(mine)
                    for sentence in self.knowledge:
                        if mine in sentence.cells:
                            sentence.mark_mine(mine)
            if sentence.known_safes():
                for safe in set(sentence.known_safes()):
                    self.mark_safe(safe)
                    for sentence in self.knowledge:
                        if safe in sentence.cells:
                            sentence.mark_safe(safe)
            # Remove sentence if it changes to be empty

            if len(sentence.cells) <= 0:
                self.knowledge.remove(sentence)

        """
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        new_sentences = []
        for sentence in self.knowledge:
            for check_sentence in self.knowledge:
                if sentence == check_sentence or sentence.cells == check_sentence.cells:
                    continue
                set1 = set(check_sentence.cells)
                set2 = set(sentence.cells)
                if set1.issubset(set2):
                    # Get all cells
                    new_cells = []
                    for cell in set2:
                        if cell not in set1:
                            new_cells.append(cell)
                    # Get count of mines
                    new_count = sentence.count - check_sentence.count
                    # Create new knowledge sentence
                    if new_count <= 0:
                        for cell in new_cells:
                            self.mark_safe(cell)
                        continue
                    if len(new_cells) == new_count:
                        for cell in new_cells:
                            self.mark_mine(cell)
                        continue
                    new_sentence = Sentence(new_cells, new_count)
                    if not new_sentence in self.knowledge:
                        new_sentences.append(new_sentence)
        for new_sentence in new_sentences:
            self.knowledge.append(new_sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) > 0:
            for cell in self.safes:
                if cell not in self.moves_made:
                    return cell
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                if cell in self.moves_made:
                    continue
                if cell in self.mines:
                    continue
                return (cell)
        return None
