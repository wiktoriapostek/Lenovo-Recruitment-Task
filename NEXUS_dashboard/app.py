import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="NEXUS Executive Dashboard",
    layout="wide"
)

st.markdown("""
<style>
@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-80px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

[data-testid="stSidebar"] {
    background: #102845;
    animation: slideInLeft 0.7s ease-out;
    min-width: 300px;
    width: 300px;
}

[data-testid="stSidebar"] > div:first-child {
    width: 300px;
}

[data-testid="stSidebar"] .block-container {
    padding-top: 1rem;
    padding-left: 0.7rem;
    padding-right: 0.7rem;
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: white !important;
}

[data-testid="stSidebar"] [data-testid="stMultiSelect"] {
    height: auto !important;
    overflow: visible !important;
}

[data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="select"] {
    height: auto !important;
    max-height: none !important;
    overflow: visible !important;
}

[data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="select"] > div {
    height: auto !important;
    max-height: none !important;
    overflow: visible !important;
    display: flex !important;
    flex-wrap: wrap !important;
    align-items: flex-start !important;
    padding: 5px 38px 5px 5px !important;
}

[data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="tag"] {
    margin: 3px !important;
}

[data-testid="stSidebar"] [data-testid="stMultiSelect"] [role="presentation"] {
    flex-wrap: wrap !important;
    overflow: visible !important;
}

[data-testid="stSidebar"] [data-testid="stMultiSelect"] input {
    min-height: 28px !important;
}

[data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="select"] > div {
    min-height: 90px !important;
}

[data-testid="stSidebar"] [data-testid="stMultiSelect"]:nth-of-type(1) [data-baseweb="select"] > div {
    min-height: 220px !important;
}

[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #D9DEE5;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    animation: fadeUp 0.7s ease-out;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    animation: fadeUp 0.7s ease-out;
}

[data-testid="stHeader"] {
    visibility: hidden;
    height: 0;
}

.main .block-container {
    padding-top: 2rem;
    animation: fadeUp 0.8s ease-out;
}

h1, h2, h3 {
    color: #102845 !important;
}

div[data-testid="stPlotlyChart"] {
    background: white;
    border-radius: 14px;
    padding: 8px;
    animation: fadeUp 0.8s ease-out;
}

.takeaway-box {
    background: white;
    border: 1px solid #D9DEE5;
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 12px;
    min-height: 105px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    animation: fadeUp 0.7s ease-out;
}
.takeaway-title {
    color: #102845;
    font-weight: 700;
    font-size: 16px;
    margin-bottom: 6px;
}

.takeaway-text {
    color: #333333;
    font-size: 14px;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

df = pd.read_csv("data/sales.csv.gz", sep=";")

st.title("NEXUS Executive Dashboard")
st.caption("Poland PC/Laptop Market | 2022–YTD 2026")
st.markdown("<hr>", unsafe_allow_html=True)

st.sidebar.header("Filters")

quarter = st.sidebar.multiselect(
    "Quarter",
    options=sorted(df["QUARTERS"].dropna().unique()),
    default=sorted(df["QUARTERS"].dropna().unique())
)

usage = st.sidebar.multiselect(
    "Usage",
    options=sorted(df["Usage"].dropna().unique()),
    default=sorted(df["Usage"].dropna().unique())
)

line = st.sidebar.multiselect(
    "LINE",
    options=sorted(df["LINE"].dropna().unique()),
    default=sorted(df["LINE"].dropna().unique())
)

segments = st.sidebar.multiselect(
    "SEGMENTS",
    options=sorted(df["SEGMENTS"].dropna().unique()),
    default=sorted(df["SEGMENTS"].dropna().unique())
)

filtered_df = df[
    df["QUARTERS"].isin(quarter) &
    df["Usage"].isin(usage) &
    df["LINE"].isin(line) &
    df["SEGMENTS"].isin(segments)
].copy()

total_units = filtered_df["SALES UNITS"].sum()
total_value = filtered_df["SALES PLN"].sum()
market_asp = total_value / total_units if total_units != 0 else 0

nexus_df = filtered_df[filtered_df["VENDOR"] == "NEXUS"]

nexus_units = nexus_df["SALES UNITS"].sum()
nexus_value = nexus_df["SALES PLN"].sum()

market_share = nexus_units / total_units if total_units != 0 else 0
nexus_asp = nexus_value / nexus_units if nexus_units != 0 else 0

st.subheader("Market Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Sales Units", f"{total_units:,.0f}")

with col2:
    st.metric("Sales Value", f"PLN {total_value:,.0f}")

with col3:
    st.metric("Market ASP", f"PLN {market_asp:,.0f}")

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("NEXUS Performance")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("NEXUS Sales Units", f"{nexus_units:,.0f}")

with col2:
    st.metric("NEXUS Market Share", f"{market_share:.1%}")

with col3:
    st.metric("NEXUS ASP", f"PLN {nexus_asp:,.0f}")

st.markdown("<br>", unsafe_allow_html=True)

trend_df = (
    filtered_df
    .groupby(["QUARTERS", "VENDOR"])["SALES UNITS"]
    .sum()
    .reset_index()
)

market_trend = (
    trend_df
    .groupby("QUARTERS")["SALES UNITS"]
    .sum()
    .reset_index(name="TOTAL_UNITS")
)

nexus_trend = (
    trend_df[trend_df["VENDOR"] == "NEXUS"]
    .groupby("QUARTERS")["SALES UNITS"]
    .sum()
    .reset_index(name="NEXUS_UNITS")
)

polaris_trend = (
    trend_df[trend_df["VENDOR"] == "POLARIS"]
    .groupby("QUARTERS")["SALES UNITS"]
    .sum()
    .reset_index(name="POLARIS_UNITS")
)

vendor_trend = (
    market_trend[["QUARTERS", "TOTAL_UNITS"]]
    .merge(nexus_trend, on="QUARTERS", how="left")
    .merge(polaris_trend, on="QUARTERS", how="left")
    .fillna(0)
)

vendor_trend["OTHERS_UNITS"] = (
    vendor_trend["TOTAL_UNITS"]
    - vendor_trend["NEXUS_UNITS"]
    - vendor_trend["POLARIS_UNITS"]
)

vendor_trend["NEXUS_SHARE"] = (
    vendor_trend["NEXUS_UNITS"] /
    vendor_trend["TOTAL_UNITS"]
)

vendor_trend["POLARIS_SHARE"] = (
    vendor_trend["POLARIS_UNITS"] /
    vendor_trend["TOTAL_UNITS"]
)

vendor_trend["OTHERS_SHARE"] = (
    vendor_trend["OTHERS_UNITS"] /
    vendor_trend["TOTAL_UNITS"]
)

st.subheader("Market Position Over Time")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("**Total Market Sales Volume Over Time**")
        fig1 = px.line(
            market_trend,
            x="QUARTERS",
            y="TOTAL_UNITS",
            markers=True
        )
        fig1.update_traces(
            line=dict(color="#e2231a", width=3),
            marker=dict(size=7)
        )
        fig1.update_layout(
            xaxis_title="Quarter",
            yaxis_title="Sales Volume",
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=10, b=20)
        )
        st.plotly_chart(
            fig1,
            use_container_width=True,
            config={"displayModeBar": False}
        )
with col2:
    with st.container(border=True):
        st.subheader("Key Takeaways")

        st.markdown(
            """
            <div class="takeaway-box">
                <div class="takeaway-title">1. NEXUS is virtually tied with POLARIS</div>
                <div class="takeaway-text">
                    Both brands hold around 25% of total market volume share.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="takeaway-box">
                <div class="takeaway-title">2. Growth was not driven by lower pricing</div>
                <div class="takeaway-text">
                    NEXUS gained market share without a consistent low-price advantage,
                    suggesting growth was driven by factors beyond relative pricing.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="takeaway-box">
                <div class="takeaway-title">3. Growth is concentrated in one key group</div>
                <div class="takeaway-text">
                    Home & Business × Consumer × Non Convertible gained
                    <b>+17.45 pp</b> in share (from 2022 to 2025) and accounts for <b>40.4%</b> of NEXUS sales.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("**Vendor Sales Volume Over Time**")
        fig5 = px.line(
            vendor_trend,
            x="QUARTERS",
            y=["NEXUS_UNITS", "POLARIS_UNITS", "OTHERS_UNITS"],
            markers=True
        )
        fig5.update_traces(
            line=dict(width=3),
            marker=dict(size=7)
        )
        fig5.for_each_trace(
            lambda trace: trace.update(
                line=dict(
                    color={
                        "NEXUS_UNITS": "#E2231A",
                        "POLARIS_UNITS": "#D98B86",
                        "OTHERS_UNITS": "#A52A2A"
                    }[trace.name],
                    width=3
                )
            )
        )
        fig5.update_layout(
            xaxis_title="Quarter",
            yaxis_title="Sales Volume",
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=10, b=20),
            legend_title="Vendor"
        )
        st.plotly_chart(
            fig5,
            use_container_width=True,
            config={"displayModeBar": False}
        )

with col2:
    with st.container(border=True):
        st.markdown("**Vendor Market Share Over Time**")
        fig6 = px.line(
            vendor_trend,
            x="QUARTERS",
            y=["NEXUS_SHARE", "POLARIS_SHARE", "OTHERS_SHARE"],
            markers=True
        )
        fig6.update_traces(
            line=dict(width=3),
            marker=dict(size=7)
        )
        fig6.for_each_trace(
            lambda trace: trace.update(
                line=dict(
                    color={
                        "NEXUS_SHARE": "#102845",
                        "POLARIS_SHARE": "#526D86",
                        "OTHERS_SHARE": "#8FA3B5"
                    }[trace.name],
                    width=3
                )
            )
        )
        fig6.update_yaxes(tickformat=".0%")
        fig6.update_layout(
            xaxis_title="Quarter",
            yaxis_title="Market Share",
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=10, b=20),
            legend_title="Vendor"
        )
        st.plotly_chart(
            fig6,
            use_container_width=True,
            config={"displayModeBar": False}
        )

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Price Band Breakdown")

price_df = filtered_df[
    (filtered_df["SALES UNITS"] > 0) &
    (filtered_df["SALES PLN"] >= 0)
].copy()

price_df["ASP"] = (
    price_df["SALES PLN"] /
    price_df["SALES UNITS"]
)

price_df["PRICE_BAND"] = pd.cut(
    price_df["ASP"],
    bins=[0, 2500, 4000, float("inf")],
    labels=["Entry", "Mainstream", "Premium"],
    include_lowest=True
)

market_band = (
    price_df
    .groupby("PRICE_BAND", observed=False)["SALES UNITS"]
    .sum()
)

market_band_share = market_band / market_band.sum()

nexus_band = (
    price_df[
        price_df["VENDOR"] == "NEXUS"
    ]
    .groupby("PRICE_BAND", observed=False)["SALES UNITS"]
    .sum()
)

nexus_band_share = (
    nexus_band / nexus_band.sum()
    if nexus_band.sum() != 0
    else nexus_band * 0
)

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("**Total Market Sales by Price Band**")
        fig3 = px.bar(
            x=market_band_share.index,
            y=market_band_share.values,
            text=market_band_share.values
        )
        fig3.update_traces(
            marker_color="#0b1f3a",
            texttemplate="%{text:.1%}"
        )
        fig3.update_yaxes(tickformat=".0%")
        fig3.update_layout(
            xaxis_title="Price Band",
            yaxis_title="Share of Sales",
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=10, b=20)
        )
        st.plotly_chart(
            fig3,
            use_container_width=True,
            config={"displayModeBar": False}
        )

with col2:
    with st.container(border=True):
        st.markdown("**NEXUS Sales by Price Band**")
        fig4 = px.bar(
            x=nexus_band_share.index,
            y=nexus_band_share.values,
            text=nexus_band_share.values
        )
        fig4.update_traces(
            marker_color="#e2231a",
            texttemplate="%{text:.1%}"
        )
        fig4.update_yaxes(tickformat=".0%")
        fig4.update_layout(
            xaxis_title="Price Band",
            yaxis_title="Share of Sales",
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=10, b=20)
        )
        st.plotly_chart(
            fig4,
            use_container_width=True,
            config={"displayModeBar": False}
        )
