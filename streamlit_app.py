import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import datetime
from fpdf import FPDF

# Page config
st.set_page_config(page_title="Netflix User Behavior Dashboard", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/netflix_titles.csv")
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['duration_int'] = df['duration'].str.extract('(\d+)').astype(float)
    df.dropna(subset=['duration_int'], inplace=True)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Data")
country_filter = st.sidebar.multiselect("Select Country", sorted(df['country'].dropna().unique()))
year_filter = st.sidebar.slider("Select Year", 2000, 2025, (2010, 2022))
genre_filter = st.sidebar.multiselect("Select Genre", sorted(set([genre for sublist in df['listed_in'].dropna().str.split(', ') for genre in sublist])))

if country_filter:
    df = df[df['country'].isin(country_filter)]
if genre_filter:
    df = df[df['listed_in'].apply(lambda x: any(g in x for g in genre_filter) if pd.notna(x) else False)]
df = df[df['date_added'].dt.year.between(year_filter[0], year_filter[1])]

# Title Section
st.markdown("""
    <h1 style='text-align: center; color: #E50914;'>🎬 Netflix User Behavior Dashboard</h1>
    <p style='text-align: center; color: gray;'>An interactive dashboard to explore trends, preferences, and content behavior</p>
""", unsafe_allow_html=True)

st.markdown("---")

# Layout
col1, col2, col3 = st.columns([1.2, 1, 1])

# COLUMN 1: Content Insights
with col1:
    st.subheader("📊 Content Type Distribution")
    content_fig = px.histogram(df, x="type", color="type",
                               color_discrete_sequence=['#E50914', '#221f1f'],
                               labels={"type": "Content Type"})
    st.plotly_chart(content_fig, use_container_width=True)

    st.subheader("📈 User Ratings Over Time")
    rating_over_time = df.dropna(subset=['date_added'])
    rating_trend = rating_over_time.groupby(rating_over_time['date_added'].dt.to_period("M")).size().reset_index(name='count')
    rating_trend['date_added'] = rating_trend['date_added'].astype(str)
    rating_fig = px.line(rating_trend, x='date_added', y='count', markers=True,
                         labels={'date_added': 'Date', 'count': 'Ratings Count'},
                         color_discrete_sequence=['#E50914'])
    st.plotly_chart(rating_fig, use_container_width=True)

# COLUMN 2: KPIs and Trends
with col2:
    st.subheader("📅 Viewing Trends")
    viewing_trend = df.dropna(subset=['date_added']).groupby(df['date_added'].dt.date).size().reset_index(name='views')
    view_trend_fig = px.area(viewing_trend, x='date_added', y='views',
                             color_discrete_sequence=['#221f1f'],
                             labels={'date_added': 'Date', 'views': 'Views'})
    st.plotly_chart(view_trend_fig, use_container_width=True)

    st.subheader("📌 Quick Stats")
    st.metric("Average Duration (mins)", f"{df['duration_int'].mean():.1f}")
    st.metric("Total Titles", df.shape[0])
    st.metric("Unique Countries", df['country'].nunique())

    st.subheader("📊 User Engagement (Estimates)")
    df['views_est'] = df['duration_int'] * 10  # Synthetic engagement metric
    engagement_df = df[['title', 'views_est']].nlargest(5, 'views_est')
    st.dataframe(engagement_df.rename(columns={'views_est': 'Estimated Views'}), use_container_width=True)

# COLUMN 3: Genre and Top Content
with col3:
    st.subheader("🍿 Genre Distribution")
    top_genres = df['listed_in'].str.split(', ').explode().value_counts().nlargest(5)
    genre_fig = px.pie(values=top_genres.values, names=top_genres.index,
                       color_discrete_sequence=px.colors.sequential.Reds,
                       hole=0.4)
    genre_fig.update_traces(textinfo='percent+label')
    st.plotly_chart(genre_fig, use_container_width=True)

    st.subheader("🌟 Top 5 Rated Titles")
    top_rated = df['title'].value_counts().head(5).reset_index()
    top_rated.columns = ['Title', 'Count']
    st.dataframe(top_rated, use_container_width=True, hide_index=True)

import os
import plotly.io as pio

# PDF Export
st.markdown("---")
st.subheader("📤 Export Dashboard Summary")

if st.button("Download PDF Summary"):
    # Create output folder
    os.makedirs("temp_figs", exist_ok=True)

    # Save charts as images
    pio.write_image(content_fig, "temp_figs/content_fig.png", format='png', width=700, height=400)
    pio.write_image(rating_fig, "temp_figs/rating_fig.png", format='png', width=700, height=400)
    pio.write_image(view_trend_fig, "temp_figs/view_trend_fig.png", format='png', width=700, height=400)
    pio.write_image(genre_fig, "temp_figs/genre_fig.png", format='png', width=700, height=400)

    # Create PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Netflix User Behavior Dashboard Summary", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)

    # Add KPIs
    pdf.cell(200, 10, txt=f"Date: {datetime.date.today().strftime('%B %d, %Y')}", ln=True)
    pdf.cell(200, 10, txt=f"Total Titles: {df.shape[0]}", ln=True)
    pdf.cell(200, 10, txt=f"Average Duration: {df['duration_int'].mean():.1f} mins", ln=True)
    pdf.cell(200, 10, txt=f"Unique Countries: {df['country'].nunique()}", ln=True)
    pdf.ln(10)

    # Add charts
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Content Type Distribution", ln=True)
    pdf.image("temp_figs/content_fig.png", w=180)
    pdf.ln(5)

    pdf.cell(200, 10, txt="User Ratings Over Time", ln=True)
    pdf.image("temp_figs/rating_fig.png", w=180)
    pdf.ln(5)

    pdf.cell(200, 10, txt="Viewing Trends", ln=True)
    pdf.image("temp_figs/view_trend_fig.png", w=180)
    pdf.ln(5)

    pdf.cell(200, 10, txt="Genre Distribution", ln=True)
    pdf.image("temp_figs/genre_fig.png", w=180)

    # Save PDF
    output_path = "Netflix_Dashboard_Full_Report.pdf"
    pdf.output(output_path)

    st.success(f"PDF Report generated: {output_path}")
    with open(output_path, "rb") as f:
        st.download_button("📥 Click to Download", data=f, file_name="Netflix_Dashboard_Full_Report.pdf")

    # Optional: Clean up temporary image files
    import shutil
    shutil.rmtree("temp_figs")


# Footer
st.markdown("---")
st.markdown("""
    <p style='text-align: center; font-size: 0.9em; color: gray;'>
    Created by Akanksha Sharma | akankshasharma2808@gmail.com | Updated: June 28, 2025
    </p>
""", unsafe_allow_html=True)
