#Project 2 - Tournament Results

Requirements - 

Writing a Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament.

The game tournament will use the Swiss system for pairing up players in each round: players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible.

To run you will also need a machine with postgres running and python psycopg2 module installed. You can download a vagrant virtual machine which has all required software [here](https://github.com/udacity/fullstack-nanodegree-vm)

In the machine, navigate to /vagrant/tournament folder and then run the following -

```
# Create tournament db and all required views/tables
psql 
\i tournament.sql

# Exit from psql
\q

# Execute the testing script
python tournament_test.py

```


Extra credit - 

* [ ] Prevent rematches between players.
* [ ] Don’t assume an even number of players. If there is an odd number of players, assign one player a “bye” (skipped round). A bye counts as a free win. A player should not receive more than one bye in a tournament.
* [x] Support games where a draw (tied game) is possible. This will require changing the arguments to reportMatch.
* [ ] When two players have the same number of wins, rank them according to OMW (Opponent Match Wins), the total number of wins by players they have played against.
* [x] Support more than one tournament in the database, so matches do not have to be deleted between tournaments. This will require distinguishing between “a registered player” and “a player who has entered in tournament #123”, so it will require changes to the database schema.
