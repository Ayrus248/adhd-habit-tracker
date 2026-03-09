import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

def prepare_data(df):
    """Clean and encode data for ML."""
    d = df.copy()
    d["Exercise"] = (d["Exercise"] == "Yes").astype(int)
    le = LabelEncoder()
    d["Mood_encoded"] = le.fit_transform(d["Mood"])
    return d

def get_correlations(df):
    """Find what habits correlate most with productivity."""
    d = prepare_data(df)
    features = ["Sleep Hours", "Exercise", "Study Hours", "Phone Usage", "Mood_encoded"]
    corr = {}
    for f in features:
        corr[f] = round(d[f].corr(d["Productivity Score"]), 2)
    return dict(sorted(corr.items(), key=lambda x: abs(x[1]), reverse=True))

def get_clusters(df):
    """Group days into behavior clusters."""
    if len(df) < 4:
        return None, None
    d = prepare_data(df)
    features = ["Sleep Hours", "Exercise", "Study Hours", "Phone Usage", "Mood_encoded"]
    X = d[features].fillna(0)
    n = min(3, len(df))
    km = KMeans(n_clusters=n, random_state=42, n_init=10)
    d["Cluster"] = km.fit_predict(X)
    centers = pd.DataFrame(km.cluster_centers_, columns=features)
    prod_by_cluster = d.groupby("Cluster")["Productivity Score"].mean()
    centers["Avg Productivity"] = prod_by_cluster.values
    return d, centers

def predict_productive_day(df):
    """Use decision tree to find what makes a productive day."""
    if len(df) < 5:
        return None, None
    d = prepare_data(df)
    features = ["Sleep Hours", "Exercise", "Study Hours", "Phone Usage", "Mood_encoded"]
    X = d[features].fillna(0)
    y = (d["Productivity Score"] >= 7).astype(int)
    if y.nunique() < 2:
        return None, None
    clf = DecisionTreeClassifier(max_depth=3, random_state=42)
    clf.fit(X, y)
    importances = dict(zip(features, clf.feature_importances_.round(3)))
    importances = dict(sorted(importances.items(), key=lambda x: x[1], reverse=True))
    return clf, importances

def get_best_worst_days(df):
    """Return the best and worst habit days."""
    best = df.loc[df["Productivity Score"].idxmax()]
    worst = df.loc[df["Productivity Score"].idxmin()]
    return best, worst