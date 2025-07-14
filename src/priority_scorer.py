def score_priority(df, user_query=""):
    df = df.copy()
    query = user_query.strip().lower()

    def calculate_score(row):
        score = 0

        score += row.get("TrustScore", 0) * 0.6

        if row.get("WebsiteHTTPS") == 1:
            score += 10

        if row.get("EmailLength", 0) > 10:
            score += 5

        score += max(0, 10 - row.get("MissingFields", 0))

        # Bonus for matching user intent
        combined_text = " ".join([
            str(row.get("Title", "")),
            str(row.get("Company", "")),
            str(row.get("Industry", "")),
            str(row.get("ProductCategory", ""))
        ]).lower()

        if query and query in combined_text:
            score += 10  # boost score if user query matches

        return round(min(score, 100), 2)

    df["PriorityScore"] = df.apply(calculate_score, axis=1)

    def label(score):
        if score >= 75:
            return "High Priority"
        elif score >= 50:
            return "Medium Priority"
        else:
            return "Low Priority"

    df["PriorityLevel"] = df["PriorityScore"].apply(label)
    return df
