import streamlit as st
import pandas as pd
import numpy as np
import joblib
from model_utils import get_trending_videos

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="YouTube Trending Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# PREMIUM UI CSS
# ==================================================
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .app-title {
        font-size: 44px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    .app-subtitle {
        font-size: 18px;
        color: #6b7280;
        margin-bottom: 20px;
    }

    .card {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.05);
        text-align: center;
    }

    .card-title {
        font-size: 14px;
        color: #6b7280;
    }

    .card-value {
        font-size: 28px;
        font-weight: 700;
        margin-top: 4px;
    }

    a.video-link {
        text-decoration: none;
        color: inherit;
        font-weight: 500;
    }

    a.video-link:hover {
        text-decoration: underline;
        color: #2563eb;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a, #020617);
        color: white;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==================================================
# SECURE API KEY
# ==================================================
api_key = st.secrets.get("YOUTUBE_API_KEY")
if not api_key:
    st.error("API key not found. Configure Streamlit secrets.")
    st.stop()

# ==================================================
# CATEGORY MAP
# ==================================================
CATEGORY_MAP = {
    "1": "Film & Animation", "2": "Autos & Vehicles", "10": "Music",
    "15": "Pets & Animals", "17": "Sports", "20": "Gaming",
    "22": "People & Blogs", "23": "Comedy", "24": "Entertainment",
    "25": "News & Politics", "26": "Howto & Style",
    "27": "Education", "28": "Science & Technology"
}

# ==================================================
# HEADER
# ==================================================
st.markdown('<div class="app-title">YouTube Trending Analytics</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Real‑time insights, growth signals & ML‑powered predictions</div>',
    unsafe_allow_html=True
)

# ==================================================
# SIDEBAR
# ==================================================
st.sidebar.markdown("## ⚙️ Dashboard Controls")

region = st.sidebar.selectbox(
    "Region",
    ["IN", "US", "CA", "GB", "JP", "DE", "FR"]
)

max_videos = st.sidebar.slider(
    "Trending Videos",
    10, 50, 50, step=5
)

st.sidebar.markdown("---")
st.sidebar.success("🔐 Secure API Connected")

# ==================================================
# LOAD ML MODELS
# ==================================================
@st.cache_resource
def load_models():
    return (
        joblib.load("random_forest_model_api.pkl"),
        joblib.load("scaler_api.pkl")
    )

rf_model, scaler = load_models()

# ==================================================
# MAIN ACTION
# ==================================================
if st.button("🚀 Analyze Trending Videos"):

    with st.spinner("Collecting YouTube data..."):
        df = get_trending_videos(api_key, region, max_videos)

    if df.empty:
        st.warning("No data returned.")
        st.stop()

    # --------------------------------------------------
    # FEATURE ENGINEERING
    # --------------------------------------------------
    df["category_name"] = df["category_id"].astype(str).map(CATEGORY_MAP).fillna("Other")
    df["youtube_url"] = "https://www.youtube.com/watch?v=" + df["video_id"]

    # ==================================================
    # KPI CARDS
    # ==================================================
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"<div class='card'><div class='card-title'>Total Videos</div>"
            f"<div class='card-value'>{len(df)}</div></div>",
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"<div class='card'><div class='card-title'>Avg Views</div>"
            f"<div class='card-value'>{int(df['views'].mean()):,}</div></div>",
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"<div class='card'><div class='card-title'>Max Views</div>"
            f"<div class='card-value'>{int(df['views'].max()):,}</div></div>",
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"<div class='card'><div class='card-title'>Avg View Velocity</div>"
            f"<div class='card-value'>{df['view_velocity'].mean():.1f}</div></div>",
            unsafe_allow_html=True
        )

    st.markdown("")

    # ==================================================
    # TABS
    # ==================================================
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📋 Videos", "📊 Analytics", "🚀 Growth", "🤖 Predictions"]
    )

    # ---------------- VIDEOS ----------------
    with tab1:
        df_v = df.copy()
        df_v["title"] = df_v.apply(
            lambda x: f'<a class="video-link" href="{x["youtube_url"]}" target="_blank">{x["title"]}</a>',
            axis=1
        )
        st.write(
            df_v[["title", "channel_title", "views", "video_age_days"]]
            .to_html(escape=False, index=False),
            unsafe_allow_html=True
        )

    # ---------------- ANALYTICS ----------------
    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("View Velocity Distribution")
            st.bar_chart(df["view_velocity"])

        with col2:
            st.subheader("Video Age vs Views")
            trend = df.groupby("video_age_days")["views"].mean().reset_index()
            st.line_chart(trend, x="video_age_days", y="views")

        st.subheader("Category Spread")
        st.bar_chart(df["category_name"].value_counts())

    # ---------------- GROWTH ----------------
    with tab3:
        gdf = df.sort_values("view_velocity", ascending=False).head(10).copy()
        gdf["title"] = gdf.apply(
            lambda x: f'<a class="video-link" href="{x["youtube_url"]}" target="_blank">{x["title"]}</a>',
            axis=1
        )
        st.write(
            gdf[["title", "views", "view_velocity"]]
            .to_html(escape=False, index=False),
            unsafe_allow_html=True
        )

    # ---------------- PREDICTIONS ----------------
    with tab4:
        X = df[["video_age_days", "title_len", "title_word_count", "tag_count"]]
        Xs = scaler.transform(X)
        probs = rf_model.predict_proba(Xs)[:, 1]

        pdf = df.copy()
        pdf["Prediction"] = np.where(probs >= 0.5, "🔥 High", "⬇ Low")
        pdf["Confidence"] = np.round(probs, 3)

        pdf["title"] = pdf.apply(
            lambda x: f'<a class="video-link" href="{x["youtube_url"]}" target="_blank">{x["title"]}</a>',
            axis=1
        )

        st.write(
            pdf[["title", "Prediction", "Confidence"]]
            .to_html(escape=False, index=False),
            unsafe_allow_html=True
        )

st.markdown("---")
st.caption("Built with YouTube Data API • Machine Learning • Streamlit")
