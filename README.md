# Head-to-Head Wins Matrix (JSON → Terminal Table)

This repo contains a Python script that reads head-to-head win/loss data from a JSON file and prints a **wins-only head-to-head matrix** (teams × teams). The output is formatted similarly to a Sports-Reference style head-to-head grid.

The solution focuses on:
- nested data structures (dictionary-of-dictionaries)
- loops and logic for building a matrix
- terminal output

---

## Input

The script expects a JSON file named `head_to_head.json` in this format:

```json
{
  "BRO": {
    "BSN": { "W": 10, "L": 12 },
    "CHC": { "W": 15, "L": 7 }
  },
  "BSN": {
    "BRO": { "W": 12, "L": 10 }
  }
}
Top-level keys = team IDs (rows)

Second-level keys = opponent IDs (columns)

Each matchup contains:

W: wins by the team vs the opponent

L: losses by the team vs the opponent

This script prints wins only (W). Losses are included in the input format but are not needed for the wins-only matrix.

Output
Rows = team

Columns = opponent

Cell value = wins by row team vs column team

Diagonal = -- (no self-matchup)

Header is printed at the top and repeated at the bottom

Example:

Tm  BRO BSN CHC ...
BRO  --  10  15 ...
BSN  12  --  13 ...
...
Tm  BRO BSN CHC ...

Approach
1) Load JSON into a nested dictionary
load_h2h() uses json.load() to read the file into a nested Python dict where:

h2h[team][opp] returns a record like {"W": 10, "L": 12}

This structure maps directly to “team → opponent → record”.

2) Build a complete team list (rows and columns)
build_teams() creates a sorted list of all teams appearing anywhere in the dataset:

start with the set of top-level keys: set(h2h.keys())

loop through each team’s opponent dictionary and add opponent keys

sort for deterministic ordering

This ensures the matrix includes teams that might appear only as opponents.

3) Construct the wins matrix with nested loops
build_wins_matrix() initializes an empty square DataFrame (teams × teams), then:

sets diagonal cells to --

fills each matchup cell with rec.get("W", "")

leaves cells blank if a matchup is missing from the JSON

4) Print in the desired table layout (with bottom header)
Pandas prints the index separately by default. To print Tm in the same header row as the team columns, the script:

copies the DataFrame

inserts the index as a real first column named Tm

resets the index to avoid printing it twice

prints using to_string(index=False)

repeats the header line at the bottom using s.splitlines()[0]

Running the Script
Requirements
Python 3.9+

pandas

Install pandas:
pip install pandas

Run:
python head_to_head_matrix.py

Files
head_to_head_matrix.py — script that loads JSON, builds the matrix, prints the table

head_to_head.json — input data file

README.md — this explanation


