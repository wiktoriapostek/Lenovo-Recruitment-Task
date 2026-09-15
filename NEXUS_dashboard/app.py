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
    from { opacity: 0; transform: translateX(-80px); }
    to   { opacity: 1; transform: translateX(0); }
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

[data-testid="stSidebar"] {
    background: #102845;
    min-width: 337px;
    width: 337px;
    animation: slideInLeft 0.7s ease-out;
}

[data-testid="stSidebar"] > div:first-child {
    width: 337px;
}

[data-testid="stSidebar"] .block-container {
    padding: 1rem 0.7rem;
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: white !important;
}

[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] [data-testid="stCheckbox"] label {
    font-size: 21px !important;
}

[data-testid="stSidebar"] [data-testid="stCheckbox"] {
    padding: 0 !important;
    margin: 0 0 -4px 0 !important;
}

[data-testid="stSidebar"] [data-testid="stCheckbox"] > label > div:first-child {
    width: 18px !important;
    height: 18px !important;
}

[data-testid="stHeader"] {
    visibility: hidden;
    height: 0;
}

.main .block-container {
    padding-top: 2rem;
    animation: fadeUp 0.8s ease-out;
}

[data-testid="stHeading"] h1 {
    font-size: 58px !important;
    color: #102845 !important;
}

[data-testid="stHeading"] h2 {
    font-size: 46px !important;
    color: #102845 !important;
}

[data-testid="stHeading"] h3 {
    font-size: 30px !important;
    color: #102845 !important;
}

.main .block-container p,
.main .block-container li,
.main .block-container label {
    font-size: 17px;
}

[data-testid="stCaptionContainer"] p {
    font-size: 18px !important;
}

[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border: 1px solid #D9DEE5;
    border-radius: 14px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    animation: fadeUp 0.7s ease-out;
}

[data-testid="stMetricValue"] {
    font-size: 44px !important;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] * {
    font-size: 21px !important;
}

[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stPlotlyChart"] {
    animation: fadeUp 0.8s ease-out;
}

div[data-testid="stPlotlyChart"] {
    background: white;
    border-radius: 14px;
    padding: 10px;
}

.takeaway-box {
    background: white;
    border: 1px solid #D9DEE5;
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 12px;
    min-height: 105px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    animation: fadeUp 0.7s ease-out;
}

.takeaway-title {
    color: #102845;
    font-weight: 700;
    font-size: 20px;
    margin-bottom: 6px;
}

.takeaway-text {
    color: #333333;
    font-size: 18px;
    line-height: 1.5;
}

.chart-title {
    color: #102845;
    font-weight: 600;
    font-size: 23px;
    line-height: 1.3;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

def sidebar_checkboxes(title, options, columns=2, key_prefix="filter"):
    st.sidebar.markdown(f"**{title}**")
    selected = []

    with st.sidebar.container(border=True):
        cols = st.columns(columns)

        for i, value in enumerate(options):
            with cols[i % columns]:
                if st.checkbox(
                    value,
                    value=True,
                    key=f"{key_prefix}_{value}"
                ):
                    selected.append(value)

    return selected


def line_layout(fig, x_values, y_title, sparse_x=False, percent=False, legend=False):
    xaxis = dict(
        title_font=dict(size=17),
        tickfont=dict(size=14),
        tickangle=-35
    )

    if sparse_x:
        xaxis.update(
            tickmode="array",
            tickvals=x_values.iloc[::2],
            ticktext=x_values.iloc[::2]
        )

    fig.update_layout(
        xaxis_title="Quarter",
        yaxis_title=y_title,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=30, r=30, t=10, b=55),
        font=dict(size=16, color="#102845"),
        xaxis=xaxis,
        yaxis=dict(
            title_font=dict(size=17),
            tickfont=dict(size=14)
        )
    )

    if percent:
        fig.update_yaxes(tickformat=".0%")

    if legend:
        fig.update_layout(
            legend_title="Vendor",
            legend=dict(
                font=dict(size=14),
                title_font=dict(size=15)
            )
        )


def bar_layout(fig):
    fig.update_layout(
        xaxis_title="Price Band",
        yaxis_title="Share of Sales",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=30, r=30, t=10, b=45),
        font=dict(size=16, color="#102845"),
        xaxis=dict(
            title_font=dict(size=17),
            tickfont=dict(size=15)
        ),
        yaxis=dict(
            title_font=dict(size=17),
            tickfont=dict(size=14)
        )
    )


def takeaway(number, title, text):
    st.markdown(
        f"""
        <div class="takeaway-box">
            <div class="takeaway-title">{number}. {title}</div>
            <div class="takeaway-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )



df = pd.read_csv("NEXUS_dashboard/data/sales.csv.gz", sep=";")



st.title("NEXUS Executive Dashboard")
st.caption("Poland PC/Laptop Market | 2022 – YTD 2026")
st.markdown("<hr>", unsafe_allow_html=True)



st.sidebar.header("Filters")

quarters = sorted(df["QUARTERS"].dropna().unique())
usage_options = sorted(df["Usage"].dropna().unique())
line_options = sorted(df["LINE"].dropna().unique())
segment_options = sorted(df["SEGMENTS"].dropna().unique())

selected_quarters = sidebar_checkboxes(
    "Quarter", quarters, columns=3, key_prefix="quarter"
)

selected_usage = sidebar_checkboxes(
    "Usage", usage_options, columns=2, key_prefix="usage"
)

selected_line = sidebar_checkboxes(
    "LINE", line_options, columns=2, key_prefix="line"
)

selected_segments = sidebar_checkboxes(
    "SEGMENTS", segment_options, columns=2, key_prefix="segment"
)

filtered_df = df[
    df["QUARTERS"].isin(selected_quarters)
    & df["Usage"].isin(selected_usage)
    & df["LINE"].isin(selected_line)
    & df["SEGMENTS"].isin(selected_segments)
].copy()



total_units = filtered_df["SALES UNITS"].sum()
total_value = filtered_df["SALES PLN"].sum()
market_asp = total_value / total_units if total_units else 0

nexus_df = filtered_df[filtered_df["VENDOR"] == "NEXUS"]

nexus_units = nexus_df["SALES UNITS"].sum()
nexus_value = nexus_df["SALES PLN"].sum()
market_share = nexus_units / total_units if total_units else 0
nexus_asp = nexus_value / nexus_units if nexus_units else 0


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

vendor_trend = (
    market_trend[["QUARTERS", "TOTAL_UNITS"]]
    .merge(
        trend_df[trend_df["VENDOR"] == "NEXUS"]
        .groupby("QUARTERS")["SALES UNITS"]
        .sum()
        .reset_index(name="NEXUS_UNITS"),
        on="QUARTERS",
        how="left"
    )
    .merge(
        trend_df[trend_df["VENDOR"] == "POLARIS"]
        .groupby("QUARTERS")["SALES UNITS"]
        .sum()
        .reset_index(name="POLARIS_UNITS"),
        on="QUARTERS",
        how="left"
    )
    .fillna(0)
)

vendor_trend["OTHERS_UNITS"] = (
    vendor_trend["TOTAL_UNITS"]
    - vendor_trend["NEXUS_UNITS"]
    - vendor_trend["POLARIS_UNITS"]
)

for vendor in ["NEXUS", "POLARIS", "OTHERS"]:
    vendor_trend[f"{vendor}_SHARE"] = (
        vendor_trend[f"{vendor}_UNITS"] / vendor_trend["TOTAL_UNITS"]
    )



st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Market Position Over Time")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown(
            '<div class="chart-title">Total Market Sales Volume Over Time</div>',
            unsafe_allow_html=True
        )

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

        line_layout(
            fig1,
            market_trend["QUARTERS"],
            "Sales Volume",
            sparse_x=False
        )

        st.plotly_chart(
            fig1,
            use_container_width=True,
            config={"displayModeBar": False}
        )

with col2:
    with st.container(border=True):
        st.subheader("Key Takeaways")

        takeaway(
            1,
            "NEXUS is virtually tied with POLARIS",
            "Both brands hold around 25% of total market volume share."
        )

        takeaway(
            2,
            "Growth was not driven by lower pricing",
            "NEXUS gained market share without a consistent low-price advantage, "
            "suggesting growth was driven by factors beyond relative pricing."
        )

        takeaway(
            3,
            "Growth is concentrated in one key group",
            "Home & Business × Consumer × Non Convertible gained "
            "<b>+17.45 pp</b> in share (from 2022 to 2025) and accounts for "
            "<b>40.4%</b> of NEXUS sales."
        )

        st.caption(
            "Strategic insights are based on the full period analysis: 2022 - YTD 2026"
        )



col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown(
            '<div class="chart-title">Vendor Sales Volume Over Time</div>',
            unsafe_allow_html=True
        )

        fig5 = px.line(
            vendor_trend,
            x="QUARTERS",
            y=["NEXUS_UNITS", "POLARIS_UNITS", "OTHERS_UNITS"],
            markers=True
        )

        colors = {
            "NEXUS_UNITS": "#E2231A",
            "POLARIS_UNITS": "#D98B86",
            "OTHERS_UNITS": "#A52A2A"
        }

        fig5.for_each_trace(
            lambda trace: trace.update(
                line=dict(color=colors[trace.name], width=3),
                marker=dict(size=7)
            )
        )

        line_layout(
            fig5,
            vendor_trend["QUARTERS"],
            "Sales Volume",
            sparse_x=True,
            legend=True
        )

        st.plotly_chart(
            fig5,
            use_container_width=True,
            config={"displayModeBar": False}
        )

with col2:
    with st.container(border=True):
        st.markdown(
            '<div class="chart-title">Vendor Market Share Over Time</div>',
            unsafe_allow_html=True
        )

        fig6 = px.line(
            vendor_trend,
            x="QUARTERS",
            y=["NEXUS_SHARE", "POLARIS_SHARE", "OTHERS_SHARE"],
            markers=True
        )

        colors = {
            "NEXUS_SHARE": "#526D86",
            "POLARIS_SHARE": "#8FA3B5",
            "OTHERS_SHARE": "#102845"
        }

        fig6.for_each_trace(
            lambda trace: trace.update(
                line=dict(color=colors[trace.name], width=3),
                marker=dict(size=7)
            )
        )

        line_layout(
            fig6,
            vendor_trend["QUARTERS"],
            "Market Share",
            sparse_x=True,
            percent=True,
            legend=True
        )

        st.plotly_chart(
            fig6,
            use_container_width=True,
            config={"displayModeBar": False}
        )



st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Price Band Breakdown")

price_df = filtered_df[
    (filtered_df["SALES UNITS"] > 0)
    & (filtered_df["SALES PLN"] >= 0)
].copy()

price_df["ASP"] = price_df["SALES PLN"] / price_df["SALES UNITS"]

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
    price_df[price_df["VENDOR"] == "NEXUS"]
    .groupby("PRICE_BAND", observed=False)["SALES UNITS"]
    .sum()
)

nexus_band_share = (
    nexus_band / nexus_band.sum()
    if nexus_band.sum()
    else nexus_band * 0
)


col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown(
            '<div class="chart-title">Total Market Sales by Price Band</div>',
            unsafe_allow_html=True
        )

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
        bar_layout(fig3)

        st.plotly_chart(
            fig3,
            use_container_width=True,
            config={"displayModeBar": False}
        )

with col2:
    with st.container(border=True):
        st.markdown(
            '<div class="chart-title">NEXUS Sales by Price Band</div>',
            unsafe_allow_html=True
        )

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
        bar_layout(fig4)

        st.plotly_chart(
            fig4,
            use_container_width=True,
            config={"displayModeBar": False}
        )
