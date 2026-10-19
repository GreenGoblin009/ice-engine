"""
Ice Engine — Daily Projected Lineups
=====================================
Reads NHL.com's "Projected lineups, starting goalies for today" article and
saves every listed player to the daily_lineups table in Supabase: who is
projected to dress and in which line / pair / goalie slot, who is scratched,
injured or suspended, and which goalie the status report says will start.

Unlike the daily pull, this is NOT an API. The article is written by hand
every day, so this script is a scraper and is deliberately strict: anything
it doesn't recognise is reported and the run exits non-zero, rather than
guessing and saving bad data. Games that parse cleanly are still saved.
The one exception is the scratched / injured / suspended lists: a line or
name there that can't be read is skipped with a warning, and the game's
lines, pairs and goalies are saved as usual.

HOW THE ARTICLE IS LAID OUT (as of October 2026) — this is what the parser
expects, and what to compare against when it starts failing:

    ## PREDATORS (1-1-1) at CANADIENS (1-1-1)
    ### 7 p.m. ET; RDS, TSN2
    Predators projected lineup
    A -- B -- C              forward lines (three names; two on a short line)
    D -- E                   defense pairs (a lone 7th defenseman is allowed)
    Goalie One               the last two single names are the goalies,
    Goalie Two               projected starter first
    Scratched: F, G
    Injured: H (lower body)
    Suspended: I             (only when there is one)
    Canadiens projected lineup
    ...
    Status report
    Free text. "... Fowler will start after being recalled ..."
    ## SATURDAY              optional: the next day's early games follow,
    ## DEVILS (4-3-0) at ... posted ahead of time; they're skipped

The text comes from the page's embedded structured data (a JSON-LD
"NewsArticle" block whose articleBody is the article in Markdown), which is
far steadier than the visible HTML.

The starting-goalie detection reads free-form sentences, so treat
confirmed_starter as "the article said so in a way this script understood".
The matched sentence is saved in the detail column so it can be checked.

POWER-PLAY UNITS are not in the article. pp_unit is worked out from the
power-play ice time the daily pull saves (player_game_logs.pp_toi): see
add_pp_units. It describes how each team has used its players lately, not
an announced plan for tonight.
"""

import argparse
import json
import os
import re
import sys
import time
import unicodedata
import urllib.request
import urllib.error
from datetime import date, datetime, timezone

import ice_engine_daily_pull as engine

LINEUPS_URL = "https://www.nhl.com/news/nhl-lineup-projections-2026-27-season"
OUT_FILE = "daily_lineups.json"

STATUS_LABELS = ("scratched", "injured", "suspended")
MIN_MATCH_RATE = 0.85  # share of dressed players that must be found in the players table
PP_GAMES = 5      # a team's most recent regular-season games that decide its power-play units
PP_UNIT_SIZE = 5  # skaters per unit

MATCHUP = re.compile(r"^(.+?)(?:\s*\([^)]*\))?\s+at\s+(.+?)(?:\s*\([^)]*\))?$", re.I)
# "## SATURDAY" (or "## SATURDAY, OCT. 17"): the games after it are another
# day's, posted early.
DAY_HEADING = re.compile(r"^(MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY)"
                         r"(?:,?\s+[A-Za-z]{3,9}\.?\s+\d{1,2})?$", re.I)
TIME_HEADING = re.compile(r"^\d{1,2}(?::\d{2})?\s*[ap]\.?m\.?\s*ET\b", re.I)
# "Ducks projected lineup" (the format so far). Also accept "Ducks lineup",
# "Ducks projected lines:" and trailing notes, in case NHL.com rewords it; a
# line that is just a team nickname is handled separately in parse_article.
TEAM_BLOCK = re.compile(r"^(.+?)(?: projected)? (?:lineup|lines)\b.*$", re.I)
LABEL = re.compile(r"^([A-Za-z][A-Za-z ]{2,24}):\s*(.*)$")
NAME_SEPARATOR = re.compile(r"\s*(?:-{2,}|[–—]+)\s*")
# Two to five words, each starting with a letter: "T.J. Hughes", "K’Andre
# Miller", "Joel Eriksson Ek", "Oliver Ekman-Larsson".
PLAYER_NAME = re.compile(r"^[^\W\d_](?:[^\W\d_]|[.'’\-])*(?: [^\W\d_](?:[^\W\d_]|[.'’\-])*){1,4}$")

# How a status report says a goalie is starting tonight ...
STARTING = re.compile(
    r"\b(?:will|expected to|set to|scheduled to|slated to|going to)\s+"
    r"(?:start|make his\b[^.;]{0,40}?\bstart|get the (?:start|nod)|be in (?:goal|net))\b"
    r"|\bgets? the (?:start|nod)\b|\bconfirmed (?:as )?the starter\b", re.I)
# ... and the look-alikes that mean the opposite, or another night.
# Checked against the clause the phrase is in (see CLAUSE), so "A will start
# and B will start on Saturday" still credits A.
NOT_TONIGHT = re.compile(
    r"\b(?:not|won't|won’t)\s+(?:expected to\s+)?start\b"
    r"|\bstart\b[^.;]{0,60}\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|tomorrow)\b"
    r"|\bstart the (?:next|second|third)\b", re.I)
CLAUSE = re.compile(r";|,?\s+(?:and|but)\s+")


class PageFormatError(Exception):
    """The article no longer looks the way this parser expects."""


def fetch_page(url, retries=3, pause=2.0):
    """GET the article HTML. NHL.com turns away clients with no browser-like
    User-Agent, hence the Mozilla prefix."""
    last_error = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (compatible; IceEngine/1.0)",
                "Accept": "text/html",
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8", "replace")
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last_error = e
            print(f"  [warn] {url} failed (attempt {attempt+1}/{retries}): {e}")
            time.sleep(pause * (attempt + 1))
    raise PageFormatError(f"could not download {url}: {last_error}")


def extract_article(html):
    """The article's Markdown text and last-modified time, from the JSON-LD
    'NewsArticle' block NHL.com embeds in the page."""
    blocks = re.findall(r'<script type="application/ld(?:\+|&#x2B;)json">(.*?)</script>', html, re.S)
    for block in blocks:
        try:
            data = json.loads(block)
        except ValueError:
            continue
        if isinstance(data, dict) and data.get("@type") == "NewsArticle" and data.get("articleBody"):
            return data["articleBody"], data.get("dateModified")
    raise PageFormatError(
        f"no NewsArticle structured data with an articleBody in the page "
        f"({len(blocks)} JSON-LD block(s), {len(html)} bytes of HTML)")


def get_schedule(day):
    """Today's games, plus the nickname the article uses for each team
    ('MAPLE LEAFS') mapped to its abbreviation ('TOR')."""
    data = engine.fetch_json(f"{engine.BASE}/schedule/{day.isoformat()}")
    games, nicknames = {}, {}
    for d in (data or {}).get("gameWeek", []):
        if d.get("date") != day.isoformat():
            continue
        for g in d.get("games", []):
            away, home = g["awayTeam"], g["homeTeam"]
            for team in (away, home):
                nicknames[team["commonName"]["default"].upper()] = team["abbrev"]
            games[(away["abbrev"], home["abbrev"])] = g["id"]
    return games, nicknames


def clean_line(raw):
    """One article line as plain text: no Markdown emphasis, escapes, heading
    marks or links, single spaces."""
    line = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", raw)
    return " ".join(re.sub(r"[*\\]", " ", line).strip().lstrip("#").split())


def split_entries(text):
    """'A (knee), B, C (upper body)' -> [('A', 'knee'), ('B', None), ...]."""
    entries = []
    for part in re.split(r",\s*(?![^()]*\))", text):
        part = part.strip()
        if not part or part.lower() == "none":
            continue
        m = re.match(r"^(.*?)\s*(?:\((.*)\))?$", part)
        entries.append((m.group(1).strip(), m.group(2)))
    return entries


def parse_article(body, schedule, nicknames, day):
    """Split the article into games and team blocks. Returns (games,
    problems, other_day): each game is {gameId, away, home, status, blocks:
    {abbrev: {lines, scratched, injured, suspended}}, problems: [...],
    warnings: [...]}. other_day lists the headings of games the article
    files under another day ("## SATURDAY"); those are left alone.

    A game with problems isn't saved. Warnings are for the scratched / injured
    / suspended lists only: a line or name there that can't be read is left
    out and the rest of the game is kept."""
    # Game headings run straight on from the previous paragraph, so put
    # every heading on a line of its own first.
    body = re.sub(r"(?<!#)(#{2,}\s)", r"\n\1", body)

    games, problems, other_day = [], [], []
    game = block = None
    in_status = False
    later_day = None  # set while under a "## SATURDAY" heading for another day

    for raw in body.splitlines():
        heading = re.match(r"\s*(#+)", raw)
        line = clean_line(raw)
        if not line:
            continue

        if heading and len(heading.group(1)) == 2 and game is not None and TIME_HEADING.match(line):
            continue  # "## 7 p.m. ET; FOXLA+, ..." is now its own heading under each game: same game, keep going

        if heading and len(heading.group(1)) == 2:  # "## AWAY (1-0-0) at HOME (0-1-0)"
            game = block = None
            in_status = False
            d = DAY_HEADING.match(line)
            if d:
                later_day = None if d.group(1).upper() == day.strftime("%A").upper() else line
                continue
            m = MATCHUP.match(line)
            if not m:
                continue  # some other section (e.g. the fantasy links at the top)
            if later_day:
                other_day.append(f"{line} ({later_day})")
                continue
            away_nick, home_nick = m.group(1).strip().upper(), m.group(2).strip().upper()
            away, home = nicknames.get(away_nick), nicknames.get(home_nick)
            if (away, home) not in schedule:
                problems.append(f"'{line}': not a game on today's schedule — the page may be "
                                f"showing another day, or the heading format changed")
                continue
            game = {"gameId": schedule[(away, home)], "away": away, "home": home,
                    "nick": {away_nick: away, home_nick: home},
                    "status": "", "blocks": {}, "problems": [], "warnings": [], "raw": []}
            games.append(game)
            continue

        if game is None:
            continue
        if len(game["raw"]) < 40:
            game["raw"].append(line)  # kept only so a failed run can show what the page looked like

        if re.fullmatch(r"status report", line, re.I):
            in_status, block = True, None
            continue

        m = TEAM_BLOCK.match(line)
        bare = game["nick"].get(line.rstrip(":").strip().upper())
        if (m or bare) and not in_status:
            team = bare or game["nick"].get(m.group(1).strip().upper())
            if team is None:
                game["problems"].append(f"'{line}': team is not one of the two playing")
                block = None
                continue
            block = {"lines": [], "scratched": [], "injured": [], "suspended": []}
            game["blocks"][team] = block
            continue

        if in_status:
            game["status"] += (" " if game["status"] else "") + line
            continue
        if block is None:
            continue  # start time / broadcasters, before the first team block

        m = LABEL.match(line)
        if m:
            # Hand-typed emphasis sometimes lands inside the word ("*I\**njured:**"
            # reads as "I njured:"), so the label is compared without its spaces.
            label = m.group(1).replace(" ", "").lower()
            if label not in STATUS_LABELS:
                game["warnings"].append(f"skipped unknown label '{m.group(1)}:' in '{line}'")
                continue
            for name, detail in split_entries(m.group(2)):
                if PLAYER_NAME.match(name):
                    block[label].append((name, detail))
                else:
                    game["warnings"].append(f"skipped '{name}' in the {label} list: not a player name")
            continue

        names = [n.strip() for n in NAME_SEPARATOR.split(line) if n.strip()]
        bad = [n for n in names if not PLAYER_NAME.match(n)]
        if bad or len(names) > 3:
            # A status list whose label is too garbled to recognise is skipped;
            # anything else unreadable could be a line, pair or goalie.
            if ":" in line or re.sub(r"[^a-z]", "", line.lower()).startswith(STATUS_LABELS):
                game["warnings"].append(f"skipped '{line}': looks like a scratched / injured list "
                                        f"but the label can't be read")
            else:
                game["problems"].append(f"can't read '{line}' as a line of player names")
            continue
        block["lines"].append(names)

    return games, problems, other_day


# First names that are one name spelled or shortened differently by different
# sources. Only needed where the first letter differs: same surname and same
# first initial already match ('Matt' / 'Matthew', 'Alexei' / 'Alexey').
FIRST_NAME_VARIANTS = [
    {"egor", "yegor"},
    {"evgeni", "evgeny", "evgenii", "yevgeni", "yevgeny", "jevgeni"},
    {"yaroslav", "jaroslav"},
    {"yakov", "jakov", "jakob", "jacob"},
    {"yuri", "juri"},
    {"alexander", "aleksander", "aleksandr", "alexandre", "alex", "oleksandr", "sasha"},
    {"alexei", "alexey", "aleksei", "oleksii"},
    {"anthony", "tony"},
    {"william", "bill", "billy"},
    {"robert", "bob", "bobby"},
    {"edward", "ted", "teddy"},
    {"theodore", "ted", "teddy"},
]


def normalize(name):
    """Name as a matching key: no accents, case, periods or apostrophes, and
    a hyphen counts as a space ("Zachary L’Heureux" == "Zachary L'Heureux",
    "J.J." == "JJ", "Sandin-Pellikka" == "Sandin Pellikka")."""
    s = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"[-‐‑–—]", " ", s)
    return " ".join(re.sub(r"[^a-z ]", "", s).split())


def same_first_name(a, b):
    """Whether two first names are one name: same first letter, or listed
    together in FIRST_NAME_VARIANTS."""
    return a[:1] == b[:1] or any(a in names and b in names for names in FIRST_NAME_VARIANTS)


def position_group(pos):
    return {"D": "D", "G": "G"}.get(pos, "F")


def find_players(name, team_players, group=None):
    """Players on the team this name could be. Exact name first (spacing
    ignored: 'De Haan' / 'DeHaan'); failing that, same surname and a first
    name that is the same name ('Matt' / 'Matthew', 'Yegor' / 'Egor'). `group`
    ('F', 'D', 'G') settles two teammates with the same name."""
    key = normalize(name)
    found = [p for p in team_players if p["key"] == key]
    if not found:
        found = [p for p in team_players if p["key"].replace(" ", "") == key.replace(" ", "")]
    if not found and " " in key:
        first, last = key.split(" ", 1)
        found = [p for p in team_players
                 if " " in p["key"] and p["key"].split(" ", 1)[1] == last
                 and same_first_name(first, p["key"].split(" ", 1)[0])]
    if len(found) > 1 and group:
        found = [p for p in found if position_group(p["pos"]) == group] or found
    return found


def build_team_rows(block, team_players):
    """Turn one team block into rows. Raises PageFormatError when the block
    doesn't have the shape of a lineup."""
    lines = block["lines"]
    if len(lines) < 9 or len(lines[-1]) != 1 or len(lines[-2]) != 1:
        raise PageFormatError(f"expected lines, pairs and then two goalies on their own lines; "
                              f"got rows of {[len(l) for l in lines]} names")

    rows, forwards, defense, seen_defense = [], [], [], False
    for names in lines[:-2]:
        groups = [position_group(p["pos"]) for n in names for p in find_players(n, team_players)[:1]]
        d, f = groups.count("D"), groups.count("F")
        if seen_defense:
            is_defense = True  # forwards are always listed first
        elif len(names) == 3:
            is_defense = False
        elif d != f:
            is_defense = d > f
        else:
            is_defense = len(forwards) >= 4  # nobody recognised: go by position in the list
        seen_defense = seen_defense or is_defense
        (defense if is_defense else forwards).append(names)

    n_f, n_d = sum(map(len, forwards)), sum(map(len, defense))
    if not (9 <= n_f <= 13 and 5 <= n_d <= 8 and 16 <= n_f + n_d <= 18):
        raise PageFormatError(f"{n_f} forwards and {n_d} defensemen is not a plausible lineup")

    def add(name, status, slot=None, number=None, group=None, detail=None):
        found = find_players(name, team_players, group)
        rows.append({
            "player_name": name,
            "player_id": found[0]["id"] if len(found) == 1 else None,
            "slot": slot,
            "slot_number": number,
            "status": status,
            "confirmed_starter": False,
            "detail": detail,
            "pp_unit": None,
        })

    for slot, group, slot_lines in (("line", "F", forwards), ("pair", "D", defense)):
        for number, names in enumerate(slot_lines, 1):
            for name in names:
                add(name, "projected", slot, number, group)
    for number, names in enumerate(lines[-2:], 1):
        add(names[0], "projected", "goalie", number, "G")
    for status in STATUS_LABELS:
        for name, detail in block[status]:
            add(name, status, detail=detail)

    wrong = [r["player_name"] for r in rows if r["slot"] == "goalie" for p in team_players
             if p["id"] == r["player_id"] and p["pos"] != "G"]
    if wrong:
        raise PageFormatError(f"{', '.join(wrong)} listed in a goalie slot but not a goalie in the players table")
    return rows


def mark_confirmed_starters(game_rows, status_text):
    """Set confirmed_starter on the goalie the status report says will
    start. Each 'will start'-type phrase is credited to the goalie named
    closest before it in the same sentence."""
    goalies = [r for r in game_rows if r["slot"] == "goalie"]
    surname = {id(r): r["player_name"].split(" ", 1)[1] for r in goalies}
    said = {}  # team -> {id(row): sentence}
    for sentence in re.split(r"\s*(?:…|\.{3}|(?<=[a-z)])\.\s+(?=[A-Z]))\s*", status_text):
        bounds = [0] + [b for m in CLAUSE.finditer(sentence) for b in (m.start(), m.end())] + [len(sentence)]
        clauses = list(zip(bounds[::2], bounds[1::2]))
        for phrase in STARTING.finditer(sentence):
            clause = next((sentence[a:b] for a, b in clauses if a <= phrase.start() < b), sentence)
            if NOT_TONIGHT.search(clause):
                continue
            before = sentence[:phrase.start()]
            mentions = [(m.start(), r) for r in goalies
                        for m in re.finditer(rf"\b{re.escape(surname[id(r)])}\b", before)]
            if mentions:
                goalie = max(mentions, key=lambda m: m[0])[1]
                said.setdefault(goalie["team"], {})[id(goalie)] = sentence.strip()
    for team, starters in said.items():
        if len(starters) != 1:
            print(f"  [warn] {team}: status report seems to name more than one starter — recording none")
            continue
        for r in goalies:
            if id(r) in starters:
                r["confirmed_starter"] = True
                r["detail"] = starters[id(r)][:300]


def add_pp_units(rows, day):
    """Set pp_unit on tonight's projected skaters: per team, the five with
    the most power-play ice time over the team's last PP_GAMES regular-season
    games before `day` are unit 1 and the next five unit 2 (fewer games early
    in the season). A skater who played none of those games for the team is
    placed by last season's power-play time instead. So the two can be
    compared, everyone is ranked on seconds per game — for the players in the
    recent games that is the same order as their totals.

    Nobody is given a unit without power-play time behind it: a team with no
    data keeps pp_unit empty, and a unit can come up short."""
    season = int(engine.season_for(day))
    last_season = season - 10001  # 20262027 -> 20252026
    regular = engine.GAME_TYPE_REGULAR
    skaters = {}
    for r in rows:
        if r["status"] == "projected" and r["slot"] in ("line", "pair") and r["player_id"]:
            skaters.setdefault(r["team"], []).append(r)

    per_game, need_last_season = {}, []
    for team, team_rows in skaters.items():
        # Newest first; 200 rows is far more than five games of one team's skaters.
        logs = engine.supabase_request(
            "GET", f"player_game_logs?select=player_id,game_id,pp_toi&team=eq.{team}&season=eq.{season}"
                   f"&game_type=eq.{regular}&pp_toi=not.is.null&game_date=lt.{day.isoformat()}"
                   f"&order=game_date.desc,game_id.desc&limit=200") or []
        recent = []
        for g in logs:
            if g["game_id"] not in recent and len(recent) < PP_GAMES:
                recent.append(g["game_id"])
        totals = {}
        for g in logs:
            if g["game_id"] in recent:
                totals[g["player_id"]] = totals.get(g["player_id"], 0) + g["pp_toi"]
        for r in team_rows:
            if r["player_id"] in totals:
                per_game[r["player_id"]] = totals[r["player_id"]] / len(recent)
            else:
                need_last_season.append(r["player_id"])

    if need_last_season:
        logs = engine.supabase_select_all(
            f"player_game_logs?select=player_id,pp_toi&season=eq.{last_season}&game_type=eq.{regular}"
            f"&pp_toi=not.is.null&player_id=in.({','.join(map(str, need_last_season))})"
            f"&order=player_id,game_id")
        played = {}
        for g in logs:
            played.setdefault(g["player_id"], []).append(g["pp_toi"])
        for player_id, seconds in played.items():
            per_game[player_id] = sum(seconds) / len(seconds)

    for team in sorted(skaters):
        ranked = sorted((r for r in skaters[team] if per_game.get(r["player_id"], 0) > 0),
                        key=lambda r: (-per_game[r["player_id"]], r["list_order"]))
        for place, r in enumerate(ranked[:2 * PP_UNIT_SIZE]):
            r["pp_unit"] = 1 + place // PP_UNIT_SIZE
        if not ranked:
            print(f"  [warn] {team}: no power-play ice time saved for these players — pp_unit left empty")
            continue
        units = [", ".join(r["player_name"] for r in ranked if r["pp_unit"] == u) for u in (1, 2)]
        print(f"  {team} PP1: {units[0]} | PP2: {units[1] or 'none'}")


def load_players(teams, use_supabase):
    """{team: [players]} from the Supabase players table. The results pull
    doesn't reach today's teams until the evening, so their current rosters
    are refreshed in the table here first — otherwise the early runs would
    miss call-ups and traded players. Without Supabase, straight from the NHL
    API so the script can still be tried locally."""
    rosters = [p for team in teams for p in engine.get_roster(team)]
    if use_supabase:
        refreshed = datetime.now(timezone.utc).isoformat(timespec="seconds")
        engine.supabase_upsert("players", [dict(p, updated_at=refreshed) for p in rosters], "id")
        players = engine.supabase_select_all(
            f"players?select=id,name,team,pos&team=in.({','.join(teams)})&order=id")
    else:
        players = rosters
    by_team = {team: [] for team in teams}
    for p in players:
        by_team[p["team"]].append(dict(p, key=normalize(p["name"])))
    return by_team


def save_to_supabase(rows, day, teams, pulled_at):
    print(f"Saving to Supabase ({engine.SUPABASE_URL}) ...")
    engine.supabase_upsert("daily_lineups", rows, "lineup_date,team,list_order")
    # A team's list can get shorter between two runs on the same day; drop
    # whatever this run didn't just rewrite.
    engine.supabase_request(
        "DELETE", f"daily_lineups?lineup_date=eq.{day.isoformat()}"
                  f"&team=in.({','.join(teams)})&updated_at=lt.{pulled_at}")


def run(day, use_supabase, late_in_day=True):
    """late_in_day: whether an article that still hasn't been updated today
    is a failure (evening) or just 'not posted yet' (midday runs)."""
    pulled_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"Ice Engine lineups — {pulled_at} (NHL date {day})")

    schedule, nicknames = get_schedule(day)
    if engine.FAILED_URLS:
        raise PageFormatError("could not load today's schedule from the NHL API")
    print(f"{len(schedule)} game(s) on today's schedule.")
    if not schedule:
        print("No games today — nothing to do.")
        return []

    body, modified = extract_article(fetch_page(LINEUPS_URL))
    if modified:
        modified_day = datetime.fromisoformat(modified[:19] + "+00:00").astimezone(engine.nhl_timezone()).date()
        print(f"Article last modified {modified} ({modified_day} Eastern), {len(body)} characters.")
        if modified_day != day:
            if late_in_day:
                raise PageFormatError(f"the article was last updated on {modified_day}, not {day} — "
                                      f"today's lineups were never posted, or the page has moved")
            print(f"Today's lineups aren't posted yet (article is from {modified_day}) — nothing to do.")
            return []

    games, problems, other_day = parse_article(body, schedule, nicknames, day)
    if not any(g["blocks"] for g in games):
        # Nothing readable: show the page's real layout in the log so the parser can be fixed.
        print(f"  [debug] article body starts: {body[:1200]!r}")
        spaced = re.sub(r"(?<!#)(#{2,}\s)", "\n\\1", body)
        heads = [ln.strip()[:90] for ln in spaced.splitlines() if ln.strip().startswith("#")]
        print(f"  [debug] heading-like lines: {heads[:20]}")
    if other_day:
        print(f"Skipping {len(other_day)} game(s) the article lists under another day: {'; '.join(other_day)}")
    if not games:
        raise PageFormatError("no game sections found in the article — the heading format "
                              "('## AWAY (w-l-otl) at HOME (w-l-otl)') has probably changed. " +
                              "; ".join(problems))

    players = load_players(sorted({t for g in games for t in (g["away"], g["home"])}), use_supabase)

    rows, saved_teams = [], []
    for g in games:
        label = f"{g['away']} at {g['home']}"
        game_rows, game_problems = [], list(g["problems"])
        for w in g["warnings"]:
            print(f"  [warn] {label}: {w}")
        for team, opponent in ((g["away"], g["home"]), (g["home"], g["away"])):
            if team not in g["blocks"]:
                game_problems.append(f"no '{team} projected lineup' section")
                print(f"  [debug] {label}: first lines the parser saw under this game: {g['raw'][:25]}")
                continue
            try:
                team_rows = build_team_rows(g["blocks"][team], players[team])
            except PageFormatError as e:
                game_problems.append(f"{team}: {e}")
                continue
            for order, r in enumerate(team_rows, 1):
                game_rows.append(dict(
                    {"lineup_date": day.isoformat(), "team": team, "list_order": order,
                     "game_id": g["gameId"], "opponent": opponent}, **r, updated_at=pulled_at))
        if game_problems:
            problems += [f"{label}: {p}" for p in game_problems]
            print(f"  {label}: NOT saved")
            continue
        mark_confirmed_starters(game_rows, g["status"])
        starters = [r["player_name"] for r in game_rows if r["confirmed_starter"]]
        print(f"  {label}: {len(game_rows)} players; confirmed starter(s): {', '.join(starters) or 'none stated'}")
        rows += game_rows
        saved_teams += [g["away"], g["home"]]

    missing = [f"{a} at {h}" for (a, h) in schedule if a not in saved_teams and
               not any(p.startswith(f"{a} at {h}:") for p in problems)]
    if missing:
        print(f"  [warn] not in the article yet: {', '.join(missing)}")

    dressed = [r for r in rows if r["status"] == "projected"]
    unmatched = [f"{r['player_name']} ({r['team']})" for r in rows if r["player_id"] is None]
    if unmatched:
        print(f"  [warn] {len(unmatched)} name(s) not found in the players table: {', '.join(unmatched)}")
    if dressed:
        rate = sum(1 for r in dressed if r["player_id"] is not None) / len(dressed)
        if rate < MIN_MATCH_RATE:
            problems.append(f"only {rate:.0%} of dressed players were found in the players table — "
                            f"has the daily pull run today, or did the name format change?")

    if use_supabase and rows:
        try:
            add_pp_units(rows, day)
        except (SystemExit, Exception) as e:
            # Units are an extra: the lineups are still worth saving without them.
            for r in rows:
                r["pp_unit"] = None
            reason = "Supabase request failed" if isinstance(e, SystemExit) else repr(e)
            print(f"  [warn] power-play units not worked out ({reason}) — saving the lineups without them")

    with open(OUT_FILE, "w") as f:
        json.dump({"pulledAt": pulled_at, "date": day.isoformat(), "lineups": rows}, f, indent=2)
    print(f"Wrote {OUT_FILE} ({len(rows)} rows)")

    if use_supabase and rows:
        save_to_supabase(rows, day, saved_teams, pulled_at)

    if problems:
        raise PageFormatError(f"{len(problems)} problem(s) reading the article:\n  - " + "\n  - ".join(problems))
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(description="Save NHL.com's projected lineups to Supabase.")
    parser.add_argument("--date", default="",
                        help="date to file the lineups under, YYYY-MM-DD; default is today (US Eastern)")
    parser.add_argument("--require-supabase", action="store_true",
                        help="fail if the Supabase env vars are missing instead of skipping the upload")
    parser.add_argument("--only-at", default="",
                        help="for scheduled runs: Eastern times to run at, e.g. '12:00,14:00'; other "
                             "triggers exit quietly (see SCHEDULE GATE in ice_engine_daily_pull.py)")
    args = parser.parse_args(argv)

    go, slot, slot_day = engine.gate_on_schedule(args.only_at)
    if not go:
        return
    day = date.fromisoformat(args.date) if args.date.strip() else (slot_day or engine.nhl_today())
    # Lineups go up through the day as teams finish their morning skates. By
    # 8 PM Eastern a page that still shows an earlier day means something broke.
    hour = slot.hour if slot else datetime.now(engine.nhl_timezone()).hour
    late_in_day = hour >= 20 or day != engine.nhl_today()

    use_supabase = bool(engine.SUPABASE_URL and engine.SUPABASE_KEY)
    if args.require_supabase and not use_supabase:
        sys.exit("SUPABASE_URL and SUPABASE_KEY must be set (see README).")
    if not use_supabase:
        print("Supabase env vars not set — matching against NHL API rosters and skipping the upload.")

    try:
        run(day, use_supabase, late_in_day)
    except PageFormatError as e:
        print(f"[error] {e}", flush=True)
        if os.environ.get("GITHUB_ACTIONS"):
            # Shows as a red annotation at the top of the workflow run.
            print(f"::error title=Lineup scrape failed::{str(e).splitlines()[0]}", flush=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
