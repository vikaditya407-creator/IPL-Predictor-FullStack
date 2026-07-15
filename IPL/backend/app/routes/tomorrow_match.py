from functools import lru_cache
from pathlib import Path
import pickle

import numpy as np
import pandas as pd
from fastapi import APIRouter
from sklearn.ensemble import RandomForestClassifier

from app.logger import logger
from app.schemas.schemas import TomorrowMatchPredictionRequest

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "predict_match_random_forest.pkl"

FEATURE_COLUMNS = [
    "team_a_form",
    "team_b_form",
    "team_a_h2h",
    "team_b_h2h",
    "team_a_stadium_win_rate",
    "team_b_stadium_win_rate",
    "avg_score",
    "bat_first_win_rate",
    "chasing_win_rate",
    "team_a_player_form",
    "team_b_player_form",
]

TEAM_ALIASES = {
    "MUMBAI INDIANS": "MI",
    "CHENNAI SUPER KINGS": "CSK",
    "ROYAL CHALLENGERS BANGALORE": "RCB",
    "ROYAL CHALLENGERS BENGALURU": "RCB",
    "KOLKATA KNIGHT RIDERS": "KKR",
    "SUNRISERS HYDERABAD": "SRH",
    "DELHI CAPITALS": "DC",
    "DELHI DAREDEVILS": "DC",
    "RAJASTHAN ROYALS": "RR",
    "GUJARAT TITANS": "GT",
    "LUCKNOW SUPER GIANTS": "LSG",
    "PUNJAB KINGS": "PBKS",
    "KINGS XI PUNJAB": "PBKS",
}

FALLBACK_TEAM_FORM = {
    "MI": 0.62,
    "CSK": 0.58,
    "RCB": 0.55,
    "KKR": 0.61,
    "SRH": 0.57,
    "DC": 0.49,
    "RR": 0.56,
    "GT": 0.53,
    "LSG": 0.51,
    "PBKS": 0.48,
}

FALLBACK_STADIUM_CONTEXT = {
    "WANKHEDE STADIUM": {
        "avg_score": 178,
        "chasing_win_rate": 0.57,
        "pitch_type": "Batting friendly red-soil pitch with good bounce",
    },
    "M. CHINNASWAMY STADIUM": {
        "avg_score": 186,
        "chasing_win_rate": 0.59,
        "pitch_type": "High-scoring batting pitch with short boundaries",
    },
    "EDEN GARDENS": {
        "avg_score": 171,
        "chasing_win_rate": 0.53,
        "pitch_type": "Balanced pitch with grip for spinners later",
    },
    "MA CHIDAMBARAM STADIUM": {
        "avg_score": 164,
        "chasing_win_rate": 0.47,
        "pitch_type": "Slow surface with spin assistance",
    },
}


def normalize_name(value: str) -> str:
    normalized = str(value).strip().upper()
    return TEAM_ALIASES.get(normalized, normalized)


def normalize_stadium(value: str) -> str:
    return str(value).strip().upper()


def find_column(frame: pd.DataFrame, candidates: list[str]) -> str | None:
    lookup = {column.lower(): column for column in frame.columns}
    for candidate in candidates:
        if candidate.lower() in lookup:
            return lookup[candidate.lower()]
    return None


def read_optional_csv(filename: str) -> pd.DataFrame:
    path = DATA_DIR / filename
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def normalize_matches(matches: pd.DataFrame) -> pd.DataFrame:
    if matches.empty:
        return matches

    column_map = {
        "date": find_column(matches, ["date", "match_date", "matchDate"]),
        "team1": find_column(matches, ["team1", "team_a", "teamA"]),
        "team2": find_column(matches, ["team2", "team_b", "teamB"]),
        "winner": find_column(matches, ["winner", "winning_team"]),
        "venue": find_column(matches, ["venue", "stadium", "stadium_name"]),
        "toss_winner": find_column(matches, ["toss_winner"]),
        "toss_decision": find_column(matches, ["toss_decision"]),
        "id": find_column(matches, ["id", "match_id"]),
    }
    required = ["date", "team1", "team2", "winner", "venue"]
    missing = [name for name in required if not column_map[name]]
    if missing:
        logger.warning(f"matches.csv missing required columns: {missing}")
        return pd.DataFrame()

    normalized = pd.DataFrame(
        {
            "date": pd.to_datetime(matches[column_map["date"]], errors="coerce"),
            "team1": matches[column_map["team1"]].map(normalize_name),
            "team2": matches[column_map["team2"]].map(normalize_name),
            "winner": matches[column_map["winner"]].map(normalize_name),
            "venue": matches[column_map["venue"]].map(normalize_stadium),
        }
    )
    normalized["match_id"] = (
        matches[column_map["id"]] if column_map["id"] else np.arange(len(matches))
    )
    normalized["toss_winner"] = (
        matches[column_map["toss_winner"]].map(normalize_name)
        if column_map["toss_winner"]
        else None
    )
    normalized["toss_decision"] = (
        matches[column_map["toss_decision"]].astype(str).str.lower()
        if column_map["toss_decision"]
        else None
    )
    return normalized.dropna(subset=["date", "team1", "team2", "winner", "venue"])


def normalize_deliveries(deliveries: pd.DataFrame) -> pd.DataFrame:
    if deliveries.empty:
        return deliveries

    column_map = {
        "match_id": find_column(deliveries, ["match_id", "id"]),
        "batting_team": find_column(deliveries, ["batting_team"]),
        "total_runs": find_column(deliveries, ["total_runs"]),
        "batsman_runs": find_column(deliveries, ["batsman_runs", "batter_runs"]),
        "batter": find_column(deliveries, ["batter", "batsman"]),
    }
    if not column_map["match_id"] or not column_map["batting_team"]:
        logger.warning("deliveries.csv missing match_id or batting_team columns")
        return pd.DataFrame()

    normalized = pd.DataFrame(
        {
            "match_id": deliveries[column_map["match_id"]],
            "batting_team": deliveries[column_map["batting_team"]].map(normalize_name),
            "total_runs": (
                pd.to_numeric(deliveries[column_map["total_runs"]], errors="coerce").fillna(0)
                if column_map["total_runs"]
                else 0
            ),
            "batsman_runs": (
                pd.to_numeric(deliveries[column_map["batsman_runs"]], errors="coerce").fillna(0)
                if column_map["batsman_runs"]
                else 0
            ),
            "batter": deliveries[column_map["batter"]] if column_map["batter"] else "",
        }
    )
    return normalized


def normalize_stadiums(stadiums: pd.DataFrame) -> pd.DataFrame:
    if stadiums.empty:
        return stadiums

    stadium_col = find_column(stadiums, ["stadium", "venue", "stadium_name"])
    pitch_col = find_column(stadiums, ["pitch_type", "soil_type", "pitch", "soil"])
    if not stadium_col or not pitch_col:
        return pd.DataFrame()

    return pd.DataFrame(
        {
            "venue": stadiums[stadium_col].map(normalize_stadium),
            "pitch_type": stadiums[pitch_col].astype(str),
        }
    )


def normalize_player_stats(player_stats: pd.DataFrame) -> pd.DataFrame:
    if player_stats.empty:
        return player_stats

    column_map = {
        "date": find_column(player_stats, ["date", "match_date", "matchDate"]),
        "team": find_column(player_stats, ["team", "team_name", "batting_team"]),
        "runs": find_column(player_stats, ["runs", "runs_scored", "batsman_runs"]),
        "wickets": find_column(player_stats, ["wickets", "wickets_taken"]),
        "match_id": find_column(player_stats, ["match_id", "id"]),
    }
    if not column_map["team"]:
        return pd.DataFrame()

    normalized = pd.DataFrame(
        {
            "team": player_stats[column_map["team"]].map(normalize_name),
            "runs": (
                pd.to_numeric(player_stats[column_map["runs"]], errors="coerce").fillna(0)
                if column_map["runs"]
                else 0
            ),
            "wickets": (
                pd.to_numeric(player_stats[column_map["wickets"]], errors="coerce").fillna(0)
                if column_map["wickets"]
                else 0
            ),
        }
    )
    normalized["date"] = (
        pd.to_datetime(player_stats[column_map["date"]], errors="coerce")
        if column_map["date"]
        else pd.NaT
    )
    normalized["match_id"] = (
        player_stats[column_map["match_id"]] if column_map["match_id"] else np.arange(len(player_stats))
    )
    return normalized


@lru_cache(maxsize=1)
def load_ipl_data() -> dict:
    matches = normalize_matches(read_optional_csv("matches.csv"))
    deliveries = normalize_deliveries(read_optional_csv("deliveries.csv"))
    players = normalize_player_stats(read_optional_csv("players.csv"))
    player_stats = normalize_player_stats(read_optional_csv("player_stats.csv"))
    if players.empty and not player_stats.empty:
        players = player_stats
    stadiums = normalize_stadiums(read_optional_csv("stadiums.csv"))

    logger.info(
        "Loaded IPL CSV resources",
        extra={
            "matches": len(matches),
            "deliveries": len(deliveries),
            "players": len(players),
            "stadiums": len(stadiums),
        },
    )

    return {
        "matches": matches,
        "deliveries": deliveries,
        "players": players,
        "stadiums": stadiums,
    }


def filter_history(matches: pd.DataFrame, match_date: str) -> pd.DataFrame:
    if matches.empty:
        return matches
    date = pd.to_datetime(match_date, errors="coerce")
    if pd.isna(date):
        return matches
    return matches[matches["date"] < date].copy()


def team_matches(matches: pd.DataFrame, team: str) -> pd.DataFrame:
    if matches.empty or "team1" not in matches or "team2" not in matches:
        return pd.DataFrame()
    return matches[(matches["team1"] == team) | (matches["team2"] == team)]


def win_rate(matches: pd.DataFrame, team: str, default: float = 0.5) -> float:
    if matches.empty or "winner" not in matches:
        return default
    return float((matches["winner"] == team).mean())


def recent_team_form(matches: pd.DataFrame, team: str, limit: int = 5) -> float:
    team_history = team_matches(matches, team)
    if team_history.empty or "date" not in team_history:
        return FALLBACK_TEAM_FORM.get(team, 0.5)
    recent = team_history.sort_values("date").tail(limit)
    return win_rate(recent, team, FALLBACK_TEAM_FORM.get(team, 0.5))


def head_to_head(matches: pd.DataFrame, team_a: str, team_b: str) -> tuple[float, float, int]:
    if matches.empty or "team1" not in matches or "team2" not in matches:
        return 0.5, 0.5, 0

    h2h = matches[
        ((matches["team1"] == team_a) & (matches["team2"] == team_b))
        | ((matches["team1"] == team_b) & (matches["team2"] == team_a))
    ]
    if h2h.empty:
        return 0.5, 0.5, 0
    return win_rate(h2h, team_a), win_rate(h2h, team_b), len(h2h)


def stadium_stats(
    matches: pd.DataFrame,
    deliveries: pd.DataFrame,
    stadium: str,
    team_a: str,
    team_b: str,
) -> dict:
    fallback = FALLBACK_STADIUM_CONTEXT.get(
        stadium,
        {
            "avg_score": 170,
            "chasing_win_rate": 0.52,
            "pitch_type": "Balanced IPL surface with moderate pace and spin support",
        },
    )

    if matches.empty or "venue" not in matches:
        return {
            "avg_score": fallback["avg_score"],
            "team_a_stadium_win_rate": 0.5,
            "team_b_stadium_win_rate": 0.5,
            "chasing_win_rate": fallback["chasing_win_rate"],
            "bat_first_win_rate": 1 - fallback["chasing_win_rate"],
        }

    stadium_matches = matches[matches["venue"] == stadium]

    avg_score = fallback["avg_score"]
    if not stadium_matches.empty and not deliveries.empty:
        innings_scores = (
            deliveries[deliveries["match_id"].isin(stadium_matches["match_id"])]
            .groupby(["match_id", "batting_team"])["total_runs"]
            .sum()
        )
        if not innings_scores.empty:
            avg_score = float(innings_scores.mean())

    team_a_stadium_win_rate = win_rate(stadium_matches, team_a, 0.5)
    team_b_stadium_win_rate = win_rate(stadium_matches, team_b, 0.5)

    if stadium_matches.empty or "toss_decision" not in stadium_matches:
        chasing_win_rate = fallback["chasing_win_rate"]
    else:
        toss_rows = stadium_matches.dropna(subset=["toss_winner", "toss_decision"])
        field_rows = toss_rows[toss_rows["toss_decision"].str.contains("field", na=False)]
        bat_rows = toss_rows[toss_rows["toss_decision"].str.contains("bat", na=False)]
        chasing_win_rate = (
            float((field_rows["winner"] == field_rows["toss_winner"]).mean())
            if not field_rows.empty
            else fallback["chasing_win_rate"]
        )
        bat_first_win_rate = (
            float((bat_rows["winner"] == bat_rows["toss_winner"]).mean())
            if not bat_rows.empty
            else 1 - chasing_win_rate
        )
        return {
            "avg_score": avg_score,
            "team_a_stadium_win_rate": team_a_stadium_win_rate,
            "team_b_stadium_win_rate": team_b_stadium_win_rate,
            "chasing_win_rate": chasing_win_rate,
            "bat_first_win_rate": bat_first_win_rate,
        }

    return {
        "avg_score": avg_score,
        "team_a_stadium_win_rate": team_a_stadium_win_rate,
        "team_b_stadium_win_rate": team_b_stadium_win_rate,
        "chasing_win_rate": chasing_win_rate,
        "bat_first_win_rate": 1 - chasing_win_rate,
    }


def recent_player_form(
    matches: pd.DataFrame,
    deliveries: pd.DataFrame,
    player_stats: pd.DataFrame,
    team: str,
    limit: int = 5,
) -> float:
    if not player_stats.empty and "team" in player_stats:
        team_players = player_stats[player_stats["team"] == team].copy()
        if not team_players.empty:
            if "date" in team_players and not team_players["date"].isna().all():
                team_players = team_players.sort_values("date").tail(limit)
            elif "match_id" in team_players:
                team_players = team_players.tail(limit)

            batting_index = team_players["runs"].mean() / 50 if "runs" in team_players else 0
            bowling_index = team_players["wickets"].mean() / 2 if "wickets" in team_players else 0
            return float(min(0.8, max(0.2, (batting_index * 0.7 + bowling_index * 0.3))))

    if matches.empty or deliveries.empty:
        return min(0.72, FALLBACK_TEAM_FORM.get(team, 0.5) + 0.04)

    team_history = team_matches(matches, team)
    if team_history.empty or "date" not in team_history or "match_id" not in team_history:
        return min(0.72, FALLBACK_TEAM_FORM.get(team, 0.5) + 0.04)

    recent_ids = team_history.sort_values("date").tail(limit)["match_id"]
    recent_deliveries = deliveries[
        (deliveries["match_id"].isin(recent_ids)) & (deliveries["batting_team"] == team)
    ]
    if recent_deliveries.empty:
        return min(0.72, FALLBACK_TEAM_FORM.get(team, 0.5) + 0.04)

    runs_per_match = recent_deliveries.groupby("match_id")["batsman_runs"].sum()
    return float(min(0.8, max(0.2, runs_per_match.mean() / 200)))


def pitch_type_for_stadium(stadiums: pd.DataFrame, stadium: str) -> str:
    fallback = FALLBACK_STADIUM_CONTEXT.get(stadium, {})
    if not stadiums.empty:
        match = stadiums[stadiums["venue"] == stadium]
        if not match.empty:
            return str(match.iloc[0]["pitch_type"])
    return fallback.get("pitch_type", "Balanced IPL surface with moderate pace and spin support")


def build_context_from_dataset(request: TomorrowMatchPredictionRequest, data: dict) -> dict:
    team_a = normalize_name(request.teamA)
    team_b = normalize_name(request.teamB)
    stadium = normalize_stadium(request.stadium)

    matches = filter_history(data["matches"], request.matchDate)
    deliveries = data["deliveries"]
    players = data["players"]
    h2h_a, h2h_b, h2h_count = head_to_head(matches, team_a, team_b)
    venue_stats = stadium_stats(matches, deliveries, stadium, team_a, team_b)

    return {
        "team_a": team_a,
        "team_b": team_b,
        "stadium": stadium,
        "team_a_form": recent_team_form(matches, team_a),
        "team_b_form": recent_team_form(matches, team_b),
        "team_a_h2h": h2h_a,
        "team_b_h2h": h2h_b,
        "h2h_count": h2h_count,
        "team_a_player_form": recent_player_form(matches, deliveries, players, team_a),
        "team_b_player_form": recent_player_form(matches, deliveries, players, team_b),
        "pitch_type": pitch_type_for_stadium(data["stadiums"], stadium),
        **venue_stats,
    }


def build_numeric_features(context: dict) -> dict:
    return {
        "team_a_form": context["team_a_form"],
        "team_b_form": context["team_b_form"],
        "team_a_h2h": context["team_a_h2h"],
        "team_b_h2h": context["team_b_h2h"],
        "team_a_stadium_win_rate": context["team_a_stadium_win_rate"],
        "team_b_stadium_win_rate": context["team_b_stadium_win_rate"],
        "avg_score": context["avg_score"],
        "bat_first_win_rate": context["bat_first_win_rate"],
        "chasing_win_rate": context["chasing_win_rate"],
        "team_a_player_form": context["team_a_player_form"],
        "team_b_player_form": context["team_b_player_form"],
    }


def features_for_match_row(row: pd.Series, data: dict) -> tuple[list[float], int] | None:
    request = TomorrowMatchPredictionRequest(
        teamA=row["team1"],
        teamB=row["team2"],
        matchDate=row["date"].strftime("%Y-%m-%d"),
        stadium=row["venue"],
    )
    context = build_context_from_dataset(request, data)
    features = build_numeric_features(context)
    target = int(row["winner"] == row["team1"])
    return [features[column] for column in FEATURE_COLUMNS], target


@lru_cache(maxsize=1)
def load_or_train_model() -> RandomForestClassifier | None:
    data = load_ipl_data()
    matches = data["matches"]

    if MODEL_PATH.exists():
        with open(MODEL_PATH, "rb") as model_file:
            return pickle.load(model_file)

    if matches.empty or len(matches) < 30:
        logger.warning("Not enough Kaggle match rows to train predict_match model")
        return None

    rows = []
    targets = []
    for _, row in matches.sort_values("date").iterrows():
        built = features_for_match_row(row, data)
        if built is None:
            continue
        features, target = built
        rows.append(features)
        targets.append(target)

    if len(rows) < 30 or len(set(targets)) < 2:
        logger.warning("Insufficient class diversity to train predict_match model")
        return None

    model = RandomForestClassifier(
        n_estimators=250,
        max_depth=8,
        min_samples_leaf=3,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(np.array(rows), np.array(targets))

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    with open(MODEL_PATH, "wb") as model_file:
        pickle.dump(model, model_file)

    logger.info(f"Trained and saved predict_match model: {MODEL_PATH}")
    return model


def fallback_probabilities(features: dict) -> tuple[int, int]:
    score = (
        0.50
        + (features["team_a_form"] - features["team_b_form"]) * 0.30
        + (features["team_a_h2h"] - features["team_b_h2h"]) * 0.20
        + (features["team_a_player_form"] - features["team_b_player_form"]) * 0.22
        + (features["team_a_stadium_win_rate"] - features["team_b_stadium_win_rate"]) * 0.15
        + ((features["avg_score"] - 165) / 40) * 0.03
        + (features["chasing_win_rate"] - 0.5) * 0.04
    )
    team_a_probability = min(0.85, max(0.15, score))
    team_a = round(team_a_probability * 100)
    return team_a, 100 - team_a


def predict_probabilities(features: dict) -> tuple[int, int]:
    model = load_or_train_model()
    if model is None:
        return fallback_probabilities(features)

    vector = np.array([[features[column] for column in FEATURE_COLUMNS]])
    probability = float(model.predict_proba(vector)[0][1])
    team_a = round(min(0.95, max(0.05, probability)) * 100)
    return team_a, 100 - team_a


@router.post("/predict_match")
async def predict_tomorrow_match(request: TomorrowMatchPredictionRequest):
    logger.info(
        "Predicting tomorrow match",
        extra={
            "teamA": request.teamA,
            "teamB": request.teamB,
            "matchDate": request.matchDate,
            "stadium": request.stadium,
        },
    )

    data = load_ipl_data()
    context = build_context_from_dataset(request, data)
    features = build_numeric_features(context)
    team_a_probability, team_b_probability = predict_probabilities(features)

    return {
        "prediction": {
            "teamA": team_a_probability,
            "teamB": team_b_probability,
        },
        "factors": {
            "team_form": (
                f"{request.teamA} recent win form {round(context['team_a_form'] * 100)}%; "
                f"{request.teamB} recent win form {round(context['team_b_form'] * 100)}%."
            ),
            "stadium_history": (
                f"{request.stadium} average score {round(context['avg_score'])}; "
                f"{request.teamA} venue win rate {round(context['team_a_stadium_win_rate'] * 100)}%, "
                f"{request.teamB} venue win rate {round(context['team_b_stadium_win_rate'] * 100)}%."
            ),
            "toss": (
                f"Bat-first success {round(context['bat_first_win_rate'] * 100)}%; "
                f"chasing success {round(context['chasing_win_rate'] * 100)}%."
            ),
            "pitch_type": context["pitch_type"],
            "player_form": (
                f"Recent batting form index: {request.teamA} "
                f"{context['team_a_player_form']:.2f}, {request.teamB} "
                f"{context['team_b_player_form']:.2f}."
            ),
        },
    }
