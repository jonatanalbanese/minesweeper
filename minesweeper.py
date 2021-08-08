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

        if len(self.cells) == self.count: 
            k_mines = self.cells
        else:
            k_mines = set()

        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return k_mines

    def known_safes(self):

        if self.count == 0:
            k_safe = self.cells
        else:
            k_safe = set()

        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return k_safe

    def mark_mine(self, cell):
        
        if cell in self.cells:
            self.cells.remove(cell)
            self.count = self.count - 1

        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
    

    def mark_safe(self, cell):

        if cell in self.cells:
            self.cells.remove(cell)

        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
    


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

    def New_info(self):

         #   mark any additional cells as safe or as mines if it can be concluded based on the AI's new knowledge

        set_mines = []
        set_safes = []
        for sentence in self.knowledge:
            if sentence.count == 0:         # Search safes cells
                for t in sentence.cells:
                    set_safes.insert(0,t)
            if sentence.count == len(sentence.cells) and sentence.count !=0:   # Search Mines
                for t in sentence.cells:
                    set_mines.insert(0,t)
        for x in set_mines:
            self.mark_mine(x)       
        for y in set_safes:
            self.mark_safe(y)     

    
    def Search_sentence(self):

        # add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge

        result_search = False
        
        for i in self.knowledge:
            for j in self.knowledge:
                if i.cells < j.cells and i.cells != set():                     
                    for t in i.cells:      
                        j.cells.remove(t)        # (ABCDE)=2 - (ABC)=1 => (DE)=1
                    j.count = j.count - i.count
                    result_search = True

        for i in self.knowledge:
            for j in i.cells:
                if j in self.safes:
                    i.cells.remove(j)       # removes safe cells from sentences
                    result_search = True
                    break

        for i in self.knowledge:
            for j in i.cells:
                if j in self.mines:
                    i.cells.remove(j)       # removes mines from sentences 
                    i.count = i.count - 1
                    result_search = True
                    break

        self.New_info()      #   mark any additional cells as safe or as mines if it can be concluded based on the AI's new knowledge

        return result_search



    def add_knowledge(self, cell, count):
        
        self.moves_made.add(cell)   # mark the cell as a move that has been made 
        
        self.mark_safe(cell)   # mark the cell as safe

        round = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    round.add((i,j))
        self.knowledge.insert(0,Sentence(round,count))   # add a new sentence to the AI's knowledge base, based on the value of `cell` and `count`
        if count == 0:      # mark the cells around as safe
            for j in round:
                self.mark_safe(j)
        if count == len(round) and count != 0:      # mark the cells around as mines
            for j in round:
                self.mark_mine(j)
        
        new_sentence = self.Search_sentence()     # add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge
        while new_sentence:
            new_sentence = self.Search_sentence()

    
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        

    def make_safe_move(self):
        
        move_ij = None
        for i in range(self.height):
            for j in range(self.width):
                if ((i , j) not in self.moves_made) and ((i , j) in self.safes):
                    move_ij = (i, j) 

        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        return move_ij

    def make_random_move(self):

        empty_1 = []
        move_ij = None
        for i in range(self.height):
            for j in range(self.width):
                if ((i , j) not in self.moves_made) and ((i , j) not in self.mines):
                    empty_1.insert(0,(i, j)) 
        if len(empty_1) > 0:
            move_ij = random.choice(empty_1)

        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        return move_ij
    
