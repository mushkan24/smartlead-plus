import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd

# -------------------------- Page Config -------------------------- #
st.set_page_config(page_title="SmartLead+", layout="wide")

# -------------------------- Dark Theme Styling -------------------------- #
st.markdown("""
    <style>
        body, .stApp {
            background: radial-gradient(circle at 25% top, #0f172a, #000000);
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
        }

        h1, h2, h3, h4 {
            color: #89c2ff;
        }

        .section-card {
            background-color: #1a1a1a;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0px 0px 10px rgba(0,255,255,0.1);
            margin-bottom: 30px;
        }

        .stButton>button {
            background-color: #3b82f6;
            color: black;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
        }

        .stTextInput>div>input {
            background-color: #111827;
            color: white;
            border: 1px solid #3b82f6;
            border-radius: 8px;
            padding: 8px;
        }

        .stSelectbox>div>div {
            background-color: #111827 !important;
            color: white !important;
        }

        .stDownloadButton > button {
            background-color: #000000 !important;
            color: #87CEFA !important;
            font-weight: 600;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            transition: all 0.3s ease;
        }

        .stDownloadButton > button:hover {
            background-color: #111111 !important;
            color: #ffffff !important;
            border: 1px solid #555;
        }

        h3, .stSelectbox label, .stTextInput label {
            color: #ffffff !important;
        }

        .reportview-container .main footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# -------------------------- App Header -------------------------- #
st.markdown("<h1 style='text-align: center; color: #87CEFA;'>SmartLead+</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>AI-Driven Trust Engine for Safer Lead Generation</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# -------------------------- Load Processed Data -------------------------- #
try:
    df = pd.read_csv("data/processed_leads.csv")

        # TrustScore calculation
    def compute_trust_score(row):
        score = 0
        score += 30 if row["WebsiteHTTPS"] else 0
        score += 20 if not row["HasDisposableDomain"] else -10
        score += 10 if row["EmailLength"] >= 12 else 0
        score += 10 if row["EmailCompanyMatch"] else -5
        return max(0, min(score, 100))

    def assign_trust_level(score):
        if score >= 70:
            return "High Trust"
        elif score >= 40:
            return "Moderate Trust"
        else:
            return "Low Trust"

    df["TrustScore"] = df.apply(compute_trust_score, axis=1)
    df["TrustLevel"] = df["TrustScore"].apply(assign_trust_level)


        # Assign numeric score based on available fields
    def compute_priority_score(row):
        score = 0
        score += 20 if row["WebsiteHTTPS"] else 0
        score += 20 if not row["HasDisposableDomain"] else -10
        score += 0 if pd.isna(row["EmailLength"]) else min(row["EmailLength"], 30)

        # Company size mapping
        size_map = {
            "1-10": 10,
            "11-50": 20,
            "51-200": 30,
            "201-500": 40,
            "501-1000": 50,
            "1001-5000": 60,
            "5001-10000": 70,
            "10000+": 80
        }
        score += size_map.get(str(row["CompanySize"]), 0)

        return min(score, 100)  # clamp max score to 100

    # Apply score and assign level
    df["PriorityScore"] = df.apply(compute_priority_score, axis=1)
    df["PriorityLevel"] = df["PriorityScore"].apply(lambda s: (
        "High Priority" if s >= 70 else
        "Medium Priority" if s >= 40 else
        "Low Priority"
    ))


    # -------------------------- Overview -------------------------- #
    st.markdown("### Scored Leads Overview")
    st.dataframe(df.head(20))  # show partial preview first

    # -------------------------- Trust Filter -------------------------- #
    st.markdown("### Filter by Trust Factors")

    trust_filter = st.selectbox("Filter by Website Security", ["All", "HTTPS Only", "Not Secure"])
    trust_df = df.copy()
    if trust_filter == "HTTPS Only":
        trust_df = trust_df[trust_df["WebsiteHTTPS"] == True]
    elif trust_filter == "Not Secure":
        trust_df = trust_df[trust_df["WebsiteHTTPS"] == False]

    # -------------------------- Priority Filter -------------------------- #
    st.markdown("### Filter by Company Size")

    company_sizes = trust_df["CompanySize"].dropna().unique().tolist()
    company_sizes.sort()
    company_size = st.selectbox("Select Company Size", ["All"] + company_sizes)

    priority_df = trust_df.copy()
    if company_size != "All":
        priority_df = priority_df[priority_df["CompanySize"] == company_size]

    # -------------------------- Keyword Search -------------------------- #
    search_input = st.text_input("Search by keyword (e.g. SaaS, Finance, CTO)")

    if search_input.strip():
        query = search_input.strip().lower()
        cols_to_search = ["Name", "Title", "Company", "Email", "Industry", "BusinessType", "ProductCategory"]
        mask = priority_df[cols_to_search].apply(lambda row: row.astype(str).str.lower().str.contains(query).any(), axis=1)
        priority_df = priority_df[mask]

    # -------------------------- Results -------------------------- #
    st.markdown(f"Leads matching all filters: `{len(priority_df)}`")

    if priority_df.empty:
        st.warning("No matching leads found.")
    else:
        priority_df = priority_df.sort_values(by="PriorityScore", ascending=False)
        priority_df = priority_df.sort_values(by="TrustScore", ascending=False)
        st.dataframe(priority_df[['Name', 'Company', 'Email', 'Industry', 'CompanySize','TrustScore', 'TrustLevel', 'PriorityScore', 'PriorityLevel']])

    # -------------------------- Download -------------------------- #
    st.download_button("Download Filtered Leads",priority_df.to_csv(index=False),"filtered_leads.csv","text/csv")

except FileNotFoundError:
    st.error("File not found! Please ensure `data/processed_leads.csv` exists.")
