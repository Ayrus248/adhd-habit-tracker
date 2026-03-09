def generate_insights(correlations, importances, df):
    """Generate human-readable insights from ML results."""
    insights = []

    # Correlation-based insights
    for habit, corr in correlations.items():
        name = habit.replace("_encoded", "").replace("_", " ")
        if corr >= 0.4:
            insights.append({
                "type": "positive",
                "icon": "✅",
                "text": f"{name} strongly boosts your productivity (correlation: +{corr})"
            })
        elif corr <= -0.4:
            insights.append({
                "type": "negative",
                "icon": "⚠️",
                "text": f"High {name} tends to reduce your productivity (correlation: {corr})"
            })
        elif 0.2 <= corr < 0.4:
            insights.append({
                "type": "neutral",
                "icon": "💡",
                "text": f"{name} has a mild positive effect on your productivity"
            })

    # Decision tree insights
    if importances:
        top = list(importances.keys())[0]
        top_name = top.replace("_encoded", "").replace("_", " ")
        insights.append({
            "type": "highlight",
            "icon": "🧠",
            "text": f"The #1 factor predicting your productive days is: {top_name}"
        })

    # Sleep-specific
    avg_sleep = df["Sleep Hours"].mean()
    if avg_sleep < 6.5:
        insights.append({
            "type": "negative",
            "icon": "😴",
            "text": f"Your average sleep is {round(avg_sleep,1)} hrs — below the recommended 7hrs for ADHD brains"
        })
    elif avg_sleep >= 7.5:
        insights.append({
            "type": "positive",
            "icon": "😴",
            "text": f"Great sleep average of {round(avg_sleep,1)} hrs — this is fueling your focus!"
        })

    # Exercise-specific
    ex_rate = (df["Exercise"] == "Yes").mean() * 100
    if ex_rate >= 60:
        insights.append({
            "type": "positive",
            "icon": "🏃",
            "text": f"You exercise {round(ex_rate)}% of days — excellent for ADHD dopamine regulation!"
        })
    elif ex_rate < 30:
        insights.append({
            "type": "negative",
            "icon": "🏃",
            "text": f"You only exercise {round(ex_rate)}% of days — even short walks can significantly help ADHD focus"
        })

    # Phone usage
    avg_phone = df["Phone Usage"].mean()
    if avg_phone > 5:
        insights.append({
            "type": "negative",
            "icon": "📱",
            "text": f"Your screen time averages {round(avg_phone,1)} hrs — consider setting app limits"
        })

    return insights