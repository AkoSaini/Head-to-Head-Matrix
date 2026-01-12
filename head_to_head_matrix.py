import json
import pandas as pd

def load_h2h(path: str) -> dict:
    """Load head-to-head JSON data: h2h[team][opp] = {'W': int, 'L': int}."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_teams(h2h: dict) -> list[str]:
    """Return a sorted list of all teams appearing as rows or opponents (robust to missing keys)."""
    teams = set(h2h.keys())
    for opponents in h2h.values():
        teams.update(opponents.keys())
    return sorted(teams)

def build_wins_matrix(h2h: dict) -> pd.DataFrame:
    """Build a wins-only head-to-head matrix (diagonal set to '--')."""
    teams = build_teams(h2h)
    df = pd.DataFrame("", index=teams, columns=teams)

    for team in teams:
        df.loc[team, team] = "--"
        for opp, rec in h2h.get(team, {}).items():
            df.loc[team, opp] = rec.get("W", "")

    df.index.name = "Tm"
    return df

if __name__ == "__main__":
    h2h = load_h2h("head_to_head.json")
    df = build_wins_matrix(h2h)

    # Makes "Tm" a real column so the header row prints as: Tm BRO BSN ...
    out = df.copy()
    out.insert(0, "Tm", out.index)
    out = out.reset_index(drop=True)

    s = out.to_string(index=False)
    print(s)
    print(s.splitlines()[0])  # repeat header at bottom
