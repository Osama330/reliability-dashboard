import streamlit as st
import pandas as pd
import plotly.express as px

def show_san_dashboard():
    st.title("📘 SAN - System Alert Notice Dashboard")

    # Load SAN data
    df = pd.read_excel("SAN.xlsx")
    df.columns = df.columns.str.strip()  # Strip whitespace

    # Filters
    years = sorted(df["YEARS"].dropna().unique())
    months = sorted(df["MONTH"].dropna().unique())
    ac_types = sorted(df["A/C TYPE"].dropna().unique())

    with st.sidebar:
        st.header("🔍 Filters")
        selected_years = st.multiselect("Select Year(s)", years, default=years)
        selected_months = st.multiselect("Select Month(s)", months, default=months)
        selected_types = st.multiselect("Select A/C Type(s)", ac_types, default=ac_types)
        etops_options = ["Show All", "Only ETOPS", "Exclude ETOPS"]
        selected_etops = st.selectbox("Include ETOPS?", etops_options)
        top_n_option = st.selectbox("Show Top:", ["All", "Top 3", "Top 6", "Top 10"], index=0)

    # Apply filters
    filtered_df = df[
        df["YEARS"].isin(selected_years) &
        df["MONTH"].isin(selected_months) &
        df["A/C TYPE"].isin(selected_types)
    ]

    if selected_etops == "Only ETOPS":
        filtered_df = filtered_df[filtered_df["ETOPS"] == True]
    elif selected_etops == "Exclude ETOPS":
        filtered_df = filtered_df[filtered_df["ETOPS"] != True]

    # =============================
    # Table: Filtered SAN Data
    # =============================
    st.subheader("📄 Filtered SAN Data")

    def highlight_rate(val, alert):
        if pd.isna(val) or pd.isna(alert):
            return ''
        return 'color: red; font-weight: bold;' if val > alert else ''

    styled_df = filtered_df.style.apply(
        lambda row: [highlight_rate(row["RATE"], row["ALERT"]) if col == "RATE" else '' for col in row.index],
        axis=1
    )
    st.dataframe(styled_df, use_container_width=True)

    # =============================
    # Chart 1: Number of SAN per ATA
    # =============================
    st.markdown("---")
    st.subheader("📊 Number of SAN per ATA Chapter")

    san_count_by_ata = filtered_df.groupby("ATA").size().reset_index(name="SAN Count")
    san_count_by_ata = san_count_by_ata.sort_values("SAN Count", ascending=False)

    if top_n_option != "All":
        n = int(top_n_option.split()[1])
        san_count_by_ata = san_count_by_ata.head(n)

    fig = px.bar(
        san_count_by_ata,
        x="SAN Count",
        y="ATA",
        orientation="h",
        text="SAN Count",
        color_discrete_sequence=["#1f77b4"],
        category_orders={"ATA": san_count_by_ata["ATA"].tolist()}
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        xaxis_title="Number of SAN",
        yaxis_title="ATA Chapter",
        xaxis_tickformat=",d",
        yaxis=dict(autorange="reversed")
    )
    st.plotly_chart(fig, use_container_width=True)

    # =============================
    # Chart 2: RATE > ALERT per ATA
    # =============================
    st.markdown("---")
    st.subheader("🚨 Exceeding Alert Threshold (RATE > ALERT) per ATA")

    alert_exceed_df = filtered_df[filtered_df["RATE"] > filtered_df["ALERT"]]
    exceed_count_by_ata = alert_exceed_df.groupby("ATA").size().reset_index(name="Exceed Count")
    exceed_count_by_ata = exceed_count_by_ata.sort_values("Exceed Count", ascending=False)

    if top_n_option != "All":
        exceed_count_by_ata = exceed_count_by_ata.head(n)

    fig2 = px.bar(
        exceed_count_by_ata,
        x="Exceed Count",
        y="ATA",
        orientation="h",
        text="Exceed Count",
        color_discrete_sequence=["#d62728"],
        category_orders={"ATA": exceed_count_by_ata["ATA"].tolist()}
    )
    fig2.update_traces(textposition="outside")
    fig2.update_layout(
        xaxis_title="Number of Exceeding Cases",
        yaxis_title="ATA Chapter",
        xaxis_tickformat=",d",
        yaxis=dict(autorange="reversed")
    )
    st.plotly_chart(fig2, use_container_width=True)

    # =============================
    # Table: % Exceeding per ATA
    # =============================
    st.markdown("---")
    st.subheader("📋 % of Exceeding Alert Threshold per ATA")

    total_counts = filtered_df.groupby("ATA").size().reset_index(name="Total SAN")
    merged = pd.merge(total_counts, exceed_count_by_ata, on="ATA", how="left").fillna(0)
    merged["Exceed %"] = round((merged["Exceed Count"] / merged["Total SAN"]) * 100, 2)

    if top_n_option != "All":
        merged = merged.sort_values("Exceed %", ascending=False).head(n)

    st.dataframe(merged, use_container_width=True)
