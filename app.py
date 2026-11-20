import io
from datetime import date

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


COLORS = {
    "navy": "#143556",
    "teal": "#2A8491",
    "gold": "#C29B4C",
    "red": "#D31F3B",
    "slate": "#5F6973",
    "light_blue": "#E8EFF4",
    "grid": "#DCE2E7",
    "canvas": "#F5F7F9",
}


st.set_page_config(
    page_title="CTICC Client Satisfaction",
    page_icon="CT",
    layout="wide",
)


@st.cache_data
def build_demo_data() -> pd.DataFrame:
    rng = np.random.default_rng(2027)
    event_names = [
        "Africa Tech Summit",
        "Cape Medical Congress",
        "Global Finance Forum",
        "Regional Tourism Expo",
        "Innovation Leadership Forum",
        "Design and Creativity Fair",
        "Energy Transition Conference",
        "Public Sector Symposium",
        "International Trade Showcase",
        "Education Futures Summit",
        "Mining and Resources Forum",
        "Hospitality Industry Awards",
    ]
    event_types = [
        "Conference",
        "Exhibition",
        "Banquet",
        "Trade Fair",
        "Film / Photo Shoot",
    ]
    venues = ["CTICC 1", "CTICC 2", "CTICC 1 + 2"]

    rows = []
    event_number = 1001
    for month in range(1, 13):
        for year in (2025, 2026):
            for _ in range(6):
                name = rng.choice(event_names)
                event_type = rng.choice(event_types)
                trend = (year - 2025) * 2.2
                season = month * 0.12
                noise = rng.normal(0, 3.8)

                scores = {
                    "Overall Satisfaction": 78 + trend + season + noise,
                    "Sales & Booking": 82 + trend + rng.normal(0, 4),
                    "Event Planning": 84 + trend + rng.normal(0, 3),
                    "Venue Facilities": 86 + trend + rng.normal(0, 3),
                    "AV & Technology": 76 + trend + rng.normal(0, 5),
                    "Catering": 83 + trend + rng.normal(0, 4),
                    "Staff Performance": 88 + trend + rng.normal(0, 2.5),
                    "Health & Safety": 89 + trend + rng.normal(0, 2),
                    "Logistics": 81 + trend + rng.normal(0, 4),
                    "Sustainability": 79 + trend + rng.normal(0, 4),
                    "Financial Administration": 80 + trend + rng.normal(0, 4),
                    "Communication": 82 + trend + rng.normal(0, 4),
                    "Event Outcomes": 77 + trend + rng.normal(0, 5),
                    "Likelihood to Recommend": 80 + trend + rng.normal(0, 5),
                }
                scores = {key: round(float(np.clip(value, 58, 98)), 1) for key, value in scores.items()}

                rows.append(
                    {
                        "Event ID": f"EV-{event_number}",
                        "Event Name": name,
                        "Event Type": event_type,
                        "Venue": rng.choice(venues),
                        "Date": pd.Timestamp(year=year, month=month, day=int(rng.integers(3, 26))),
                        "Responses": int(rng.integers(8, 31)),
                        "NPS": int(np.clip(round(scores["Likelihood to Recommend"] - 18), -20, 85)),
                        **scores,
                    }
                )
                event_number += 1

    df = pd.DataFrame(rows)
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.strftime("%b")
    df["Month Number"] = df["Date"].dt.month
    df["Benchmark"] = 80.0
    df["Status"] = np.where(df["Overall Satisfaction"] >= df["Benchmark"], "Meets Benchmark", "Below Benchmark")
    df["Quarter"] = "Q" + df["Date"].dt.quarter.astype(str)
    return df


def export_excel(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Event Summary", index=False)
    return output.getvalue()


df = build_demo_data()

st.title("Client Satisfaction Intelligence")
st.caption("Demonstration using anonymised dummy data | CTICC")

with st.sidebar:
    st.markdown("### Filters")
    selected_year = st.multiselect("Reporting year", sorted(df["Year"].unique(), reverse=True), default=[2026])
    selected_quarter = st.multiselect(
        "Quarter",
        ["Q1", "Q2", "Q3", "Q4"],
        default=["Q1", "Q2", "Q3", "Q4"],
    )
    selected_types = st.multiselect(
        "Event type",
        sorted(df["Event Type"].unique()),
        default=sorted(df["Event Type"].unique()),
    )
    benchmark = st.slider("Benchmark score", 60, 90, 80)

filtered = df[
    df["Year"].isin(selected_year)
    & df["Quarter"].isin(selected_quarter)
    & df["Event Type"].isin(selected_types)
].copy()
filtered["Benchmark"] = float(benchmark)
filtered["Status"] = np.where(
    filtered["Overall Satisfaction"] >= benchmark,
    "Meets Benchmark",
    "Below Benchmark",
)

st.markdown(
    f"""
    <style>
    [data-testid="stTabs"] [role="tablist"] {{
        gap: 0.45rem;
        border-bottom: 1px solid {COLORS["grid"]};
        padding-bottom: 0.4rem;
    }}
    [data-testid="stTabs"] [data-testid="stTab"] {{
        background: {COLORS["light_blue"]};
        color: {COLORS["navy"]};
        border: 1px solid {COLORS["grid"]};
        border-radius: 8px 8px 0 0;
        padding: 0.55rem 0.9rem;
        transition: background-color 120ms ease, color 120ms ease;
    }}
    [data-testid="stTabs"] [data-testid="stTab"] p {{
        color: inherit;
        font-weight: 600;
    }}
    [data-testid="stTabs"] [data-testid="stTab"]:hover {{
        background: #D3EBEE;
        color: {COLORS["navy"]};
    }}
    [data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"] {{
        background: {COLORS["navy"]};
        color: #FFFFFF;
        border-color: {COLORS["navy"]};
        box-shadow: inset 0 -3px 0 {COLORS["gold"]};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

tab_dashboard, tab_events, tab_reports, tab_guide = st.tabs(
    ["Executive Dashboard", "Event Search", "Reports & Evidence", "User Guide"]
)

with tab_dashboard:
    st.subheader("Performance Overview")

    with st.container(horizontal=True):
        st.metric(
            "Average satisfaction",
            f"{filtered['Overall Satisfaction'].mean():.1f}",
            f"{(filtered['Overall Satisfaction'].mean() - benchmark):+.1f} vs benchmark",
            border=True,
        )
        st.metric(
            "Net Promoter Score",
            f"{filtered['NPS'].mean():.0f}",
            f"{len(filtered):,} events",
            border=True,
        )
        st.metric(
            "Below benchmark",
            f"{(filtered['Status'] == 'Below Benchmark').sum()}",
            f"{(filtered['Status'] == 'Below Benchmark').mean():.1%} of events",
            border=True,
        )
        st.metric(
            "Survey responses",
            f"{filtered['Responses'].sum():,}",
            "Dummy data",
            border=True,
        )

    left, right = st.columns((2, 1), gap="medium")
    with left:
        monthly = (
            filtered.groupby(["Year", "Month Number", "Month"], as_index=False)["Overall Satisfaction"]
            .mean()
            .sort_values(["Year", "Month Number"])
        )
        fig = px.line(
            monthly,
            x="Month",
            y="Overall Satisfaction",
            color="Year",
            markers=True,
            color_discrete_map={2025: COLORS["slate"], 2026: COLORS["red"]},
        )
        fig.add_hline(
            y=benchmark,
            line_dash="dash",
            line_color=COLORS["gold"],
            annotation_text=f"Benchmark {benchmark}",
        )
        fig.update_layout(
            title="Monthly Satisfaction Trend",
            yaxis_range=[65, 100],
            legend_title="",
            hovermode="x unified",
            paper_bgcolor=COLORS["canvas"],
            plot_bgcolor=COLORS["canvas"],
            font_color=COLORS["navy"],
            xaxis_gridcolor=COLORS["grid"],
            yaxis_gridcolor=COLORS["grid"],
            margin=dict(l=20, r=20, t=60, b=20),
        )
        with st.container(border=True):
            st.plotly_chart(fig, use_container_width=True)

    with right:
        score_columns = [
            "Event Planning",
            "Venue Facilities",
            "Catering",
            "AV & Technology",
            "Communication",
            "Staff Performance",
        ]
        area_scores = filtered[score_columns].mean().sort_values()
        fig2 = go.Figure(
            go.Bar(
                x=area_scores.values,
                y=area_scores.index,
                orientation="h",
                marker_color=[
                    COLORS["red"] if x < benchmark else COLORS["teal"]
                    for x in area_scores
                ],
                text=[f"{x:.1f}" for x in area_scores.values],
                textposition="outside",
            )
        )
        fig2.add_vline(x=benchmark, line_dash="dash", line_color=COLORS["gold"])
        fig2.update_layout(
            title="Priority Service Areas",
            xaxis_range=[65, 100],
            paper_bgcolor=COLORS["canvas"],
            plot_bgcolor=COLORS["canvas"],
            font_color=COLORS["navy"],
            xaxis_gridcolor=COLORS["grid"],
            margin=dict(l=20, r=20, t=60, b=20),
        )
        with st.container(border=True):
            st.plotly_chart(fig2, use_container_width=True)

    quarter_data = (
        filtered.groupby(["Quarter", "Year"], as_index=False)["Overall Satisfaction"]
        .mean()
        .sort_values(["Year", "Quarter"])
    )
    comparison = (
        filtered.groupby("Quarter", as_index=False)
        .agg(
            Satisfaction=("Overall Satisfaction", "mean"),
            Responses=("Responses", "sum"),
            Below_Benchmark=("Status", lambda s: (s == "Below Benchmark").sum()),
        )
        .sort_values("Quarter")
    )

    chart_col, alert_col = st.columns((2, 1), gap="medium")
    with chart_col:
        fig3 = px.bar(
            comparison,
            x="Quarter",
            y="Satisfaction",
            color="Quarter",
            text=comparison["Satisfaction"].round(1),
            color_discrete_sequence=[
                COLORS["navy"],
                COLORS["teal"],
                COLORS["gold"],
                COLORS["red"],
            ],
        )
        fig3.add_hline(y=benchmark, line_dash="dash", line_color=COLORS["slate"])
        fig3.update_layout(
            title="Quarterly Comparison",
            yaxis_range=[65, 100],
            showlegend=False,
            paper_bgcolor=COLORS["canvas"],
            plot_bgcolor=COLORS["canvas"],
            font_color=COLORS["navy"],
            xaxis_gridcolor=COLORS["grid"],
            yaxis_gridcolor=COLORS["grid"],
            margin=dict(l=20, r=20, t=60, b=20),
        )
        with st.container(border=True):
            st.plotly_chart(fig3, use_container_width=True)

    with alert_col:
        with st.container(border=True):
            st.subheader("Benchmark Alerts")
            under = filtered[filtered["Status"] == "Below Benchmark"].sort_values(
                "Overall Satisfaction"
            )
            st.metric("Events requiring action", len(under), border=True)
            if not under.empty:
                alert_table = under[
                    ["Event ID", "Event Name", "Date", "Overall Satisfaction"]
                ].head(6)
                alert_table["Date"] = alert_table["Date"].dt.strftime("%d %b %Y")
                st.dataframe(
                    alert_table,
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "Overall Satisfaction": st.column_config.ProgressColumn(
                            "Score",
                            min_value=60,
                            max_value=100,
                            format="%.1f",
                        )
                    },
                )
            else:
                st.success("No events are below the selected benchmark.")

with tab_events:
    st.subheader("Search Current and Historical Events")

    search = st.text_input("Search event name or event ID", placeholder="Try EV-1 or Africa")
    event_table = filtered.copy()
    if search.strip():
        needle = search.strip().lower()
        event_table = event_table[
            event_table["Event Name"].str.lower().str.contains(needle, regex=False)
            | event_table["Event ID"].str.lower().str.contains(needle, regex=False)
        ]

    selected_status = st.pills(
        "Status",
        ["All", "Meets Benchmark", "Below Benchmark"],
        selection_mode="single",
        default="All",
    )
    if selected_status != "All":
        event_table = event_table[event_table["Status"] == selected_status]

    display_columns = [
        "Event ID",
        "Event Name",
        "Event Type",
        "Venue",
        "Date",
        "Responses",
        "Overall Satisfaction",
        "NPS",
        "Status",
    ]
    event_table["Date"] = event_table["Date"].dt.strftime("%d %b %Y")

    st.dataframe(
        event_table[display_columns],
        hide_index=True,
        use_container_width=True,
        height=430,
        column_config={
            "Overall Satisfaction": st.column_config.ProgressColumn(
                "Satisfaction",
                min_value=60,
                max_value=100,
                format="%.1f",
            ),
            "NPS": st.column_config.NumberColumn("NPS", format="%d"),
        },
    )

    if not event_table.empty:
        event_ids = event_table["Event ID"].tolist()
        selected_event_id = st.selectbox("Open an event report", event_ids)
        selected_event = event_table[event_table["Event ID"] == selected_event_id].iloc[0]

        st.markdown("#### Individual Client Interview Report")
        c1, c2, c3 = st.columns(3)
        c1.write(f"**Event:** {selected_event['Event Name']}")
        c2.write(f"**Venue:** {selected_event['Venue']}")
        c3.write(f"**Survey responses:** {selected_event['Responses']}")

        detail_scores = {
            col: selected_event[col]
            for col in df.columns
            if col not in [
                "Event ID", "Event Name", "Event Type", "Venue", "Date", "Responses",
                "NPS", "Year", "Month", "Month Number", "Benchmark", "Status",
                "Quarter",
            ]
        }
        detail_df = pd.DataFrame(
            {"Evaluation Area": detail_scores.keys(), "Score": detail_scores.values()}
        )
        detail_df["Benchmark"] = benchmark
        detail_df["Variation"] = detail_df["Score"] - benchmark
        st.dataframe(detail_df, hide_index=True, use_container_width=True)

with tab_reports:
    st.subheader("Reports, Evidence and Data Migration")

    report_col, evidence_col = st.columns((1.25, 1), gap="medium")
    with report_col:
        with st.container(border=True):
            st.markdown("**Generate a report**")
            report_period = st.radio(
                "Reporting period",
                ["Monthly", "Quarterly", "Annual", "Ad-hoc"],
                horizontal=True,
            )
            st.download_button(
                "Download filtered report (Excel)",
                data=export_excel(filtered),
                file_name="cticc_client_satisfaction_demo.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
            st.caption(f"The export includes {len(filtered):,} anonymised event records.")

    with evidence_col:
        with st.container(border=True):
            st.markdown("**Evidence and corrective action**")
            if "saved_evidence" not in st.session_state:
                st.session_state.saved_evidence = ""
            evidence = st.text_area(
                "Management note",
                value=st.session_state.saved_evidence,
                placeholder="Enter an improvement action or supporting evidence...",
                height=120,
            )
            if st.button("Save evidence", use_container_width=True):
                st.session_state.saved_evidence = evidence
                st.success("Evidence saved for this demo session.")

    migration_col, training_col = st.columns(2, gap="medium")
    with migration_col:
        with st.container(border=True):
            st.subheader("Historical Data Migration")
            st.markdown(
                """
                1. Extract existing survey data and reports  
                2. Validate event identifiers and historical benchmarks  
                3. Map and cleanse survey dimensions  
                4. Import data with audit trails  
                5. Reconcile totals and sign off with CTICC  
                """
            )

    with training_col:
        with st.container(border=True):
            st.subheader("Training Options")
            st.markdown(
                """
                - Platform administrator training
                - Executive dashboard briefing
                - Report interpretation workshop
                - Customer-experience improvement workshop
                - On-demand refresher sessions
                """
            )

with tab_guide:
    st.subheader("Demo User Guide")

    st.markdown(
        """
        ### Executive dashboard
        Use the sidebar to select reporting years, quarters, event types, and the benchmark score.
        The KPI cards, charts, and alerts update automatically.

        ### Event search
        Search by event name or event ID, filter by benchmark status, and open an individual
        event report. The report shows each evaluation area and its variation from the benchmark.

        ### Reports and evidence
        Download the filtered event set as an Excel workbook. Management notes can be entered
        and saved for the active demo session.

        ### Demo limitations
        This is a non-production showcase containing anonymised dummy data. It demonstrates
        the proposed interface and user journeys. Authentication, data storage, report publishing,
        workflow approvals, and migration integrations can be configured for the final platform.
        """
    )
