import pandas as pd
import os
from datetime import date

DATA_PATH = "data/habits.csv"

def load_data():
    """Load all habit data from CSV."""
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH, encoding='utf-8')
        if not df.empty:
            df["Date"] = pd.to_datetime(df["Date"], format='mixed')
        return df
    else:
        # Return empty dataframe with correct columns
        return pd.DataFrame(columns=[
            "Date", "Sleep Hours", "Exercise",
            "Study Hours", "Phone Usage", "Mood", "Productivity Score"
        ])

def save_entry(date_val, sleep, exercise, study, phone, mood, productivity):
    """Save a single day's habit entry."""
    df = load_data()

    # Check if entry for this date already exists
    if not df.empty and str(date_val) in df["Date"].astype(str).values:
        return False, "⚠️ Entry for this date already exists!"

    new_row = {
        "Date": str(date_val).split(" ")[0],
        "Sleep Hours": sleep,
        "Exercise": exercise,
        "Study Hours": study,
        "Phone Usage": phone,
        "Mood": mood,
        "Productivity Score": productivity
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)
    return True, "✅ Entry saved successfully!"

def get_last_n_days(n=7):
    """Get the last N days of data."""
    df = load_data()
    if df.empty:
        return df
    df = df.sort_values("Date", ascending=False)
    return df.head(n)

def get_all_data():
    """Return all data sorted by date."""
    df = load_data()
    if df.empty:
        return df
    return df.sort_values("Date", ascending=True)