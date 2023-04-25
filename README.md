## **week0 - Search**

## degrees

#### **_Background_**

> According to the Six Degrees of Kevin Bacon game, anyone in the Hollywood film industry can be connected to Kevin Bacon within six steps, where each step consists of finding a film that two actors both starred in.

> In this problem, we’re interested in finding the shortest path between any two actors by choosing a sequence of movies that connects them. For example, the shortest path between Jennifer Lawrence and Tom Hanks is 2: Jennifer Lawrence is connected to Kevin Bacon by both starring in “X-Men: First Class,” and Kevin Bacon is connected to Tom Hanks by both starring in “Apollo 13.”

> We can frame this as a search problem: our states are people. Our actions are movies, which take us from one actor to another (it’s true that a movie could take us to multiple different actors, but that’s okay for this problem). Our initial state and goal state are defined by the two people we’re trying to connect. By using breadth-first search, we can find the shortest path from one actor to another.

#### **_About_**

The distribution code contains two sets of CSV data files:

- one set in the large directory
- one set in the small directory.
  Each contains files with the same names, and the same structure, but small is a much smaller dataset for ease of testing and experimentation.

#### **_How to start_**

Go into the directory _"degrees"_

```
$ cd week0/degrees/
```

If you want to run the **small** dataset

```
$ python3 degrees.py small
```

If you want to run the **large** dataset

```
$ python3 degrees.py large
```

Now enter two different actor names to find the degree of separation.

Open up `small/people.csv` or `large/people.csv` to see which actors are available for your curent set.

#### **_Result_**

```
Loading data...
Data loaded.
Name: Doris Day
Name: Federico Fellini
Searching...
Explored Steps: 1801
3 degrees of separation.
1: Doris Day and Clint Eastwood starred in Don't Pave Main Street: Carmel's Heritage
2: Clint Eastwood and Bernardo Bertolucci starred in Kurosawa's Way
3: Bernardo Bertolucci and Federico Fellini starred in Bellissimo: Immagini del cinema italiano
```

## tictactoe

#### **_About_**

Using Minimax, implement an AI to play Tic-Tac-Toe optimally.

#### **_Getting Started_**

Once in the directory for the project, run `pip3 install -r requirements.txt` to install the required Python package (`pygame`) for this project.

#### **_How to start:_**

Go into the directory _"degrees"_

```
$ cd week0/degrees/
```

To run the game run:

```
$ python3 runner.py
```

#### **_Game_**

| Menu                                     | Ingame                                   |
| ---------------------------------------- | ---------------------------------------- |
| ![tictactoe menu](images/tictactoe0.png) | ![tictactoe game](images/tictactoe1.png) |

## week1 - Knowledge

### knights

### minesweeper

## week2 - Uncertainty

### heredity

### pagerank

## week3 - Optimization

### crossword
