import pandas as pd
import numpy as np
from datetime import datetime, timezone
from googleapiclient.discovery import build
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib

API_KEY = "AIzaSyAFliih-ajEj1b9r9XIbV0BiaeDEMO6Vjw"

youtube = build("youtube", "v3", developerKey=API_KEY)

def get_trending_videos(region="IN", max_results=200):
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode=region,
        maxResults=max_results
    )
    response = request.execute()

    records = []

    for item in response["items"]:
        records.append({
            "video_id": item["id"],
            "title": item["snippet"]["title"],
            "publish_time": item["snippet"]["publishedAt"],
            "category_id": item["snippet"]["categoryId"],
            "views": int(item["statistics"].get("viewCount", 0)),
            "tags": "|".join(item["snippet"].get("tags", []))
        })

    df = pd.DataFrame(records)
    df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
    df["trending_date"] = pd.Timestamp.now(tz=timezone.utc)

    df["video_age_days"] = (df["trending_date"] - df["publish_time"]).dt.days
    df["title_len"] = df["title"].astype(str).apply(len)
    df["title_word_count"] = df["title"].astype(str).apply(lambda x: len(x.split()))

    def tag_count(tags):
        if pd.isna(tags) or tags == "":
            return 0
        return len(tags.split("|"))

    df["tag_count"] = df["tags"].apply(tag_count)

    threshold = df["views"].quantile(0.90)
    df["high_engagement"] = (df["views"] >= threshold).astype(int)

    num_features = ["video_age_days", "title_len", "title_word_count", "tag_count"]
    X = df[num_features].fillna(0)
    y = df["high_engagement"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    rf.fit(X_train_scaled, y_train)

    joblib.dump(rf, "random_forest_model_api.pkl")
    joblib.dump(scaler, "scaler_api.pkl")

    print("Training complete. Models saved!")

if __name__ == "__main__":
    get_trending_videos()
