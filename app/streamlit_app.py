from pathlib import Path
import sys
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.analysis import clean_data, aggregate_products, aggregate_divisions, pareto, margin_volatility, factory_summary, FACTORIES, PRODUCT_FACTORY, validation_report

st.set_page_config(page_title="Nassau Candy | Profitability Intelligence", page_icon="🍬", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root { --ink:#eef3ff; --muted:#9aa8c7; --panel:#141d33; --panel2:#192440; --accent:#ffcc66; --cyan:#5de2e7; --purple:#9b8cff; --danger:#ff7891; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: radial-gradient(circle at 10% 0%, rgba(93,226,231,.12), transparent 27%), radial-gradient(circle at 95% 10%, rgba(155,140,255,.16), transparent 26%), #0b1020; color:var(--ink); }
.block-container { padding: 2rem 3rem 3rem; max-width: 1600px; }
h1,h2,h3 { font-family:'Space Grotesk', sans-serif; letter-spacing:-.02em; }
h1 { font-size:2.5rem; }
.hero { padding: 1.4rem 1.7rem; border:1px solid rgba(255,255,255,.1); border-radius:24px; background:linear-gradient(120deg, rgba(20,29,51,.96), rgba(25,36,64,.78)); box-shadow:0 18px 50px rgba(0,0,0,.22); margin-bottom:1.2rem; position:relative; overflow:hidden; }
.hero:after { content:'✦  ·  🍬  ·  ✧  ·  🍭  ·  ✦'; position:absolute; right:2rem; top:1.8rem; color:rgba(255,204,102,.24); font-size:1.3rem; letter-spacing:1.2rem; }
.eyebrow { color:var(--cyan); font-size:.74rem; text-transform:uppercase; letter-spacing:.16em; font-weight:700; }
.subtle { color:var(--muted); }
.kpi { background:linear-gradient(145deg, rgba(25,36,64,.95), rgba(20,29,51,.96)); border:1px solid rgba(255,255,255,.08); border-radius:18px; padding:1rem 1.1rem; min-height:105px; }
.kpi-label { color:var(--muted); font-size:.78rem; text-transform:uppercase; letter-spacing:.08em; }
.kpi-value { color:var(--ink); font-family:'Space Grotesk'; font-size:1.7rem; font-weight:700; margin-top:.4rem; }
.kpi-note { color:var(--accent); font-size:.75rem; margin-top:.2rem; }
.section { border-top:1px solid rgba(255,255,255,.08); padding-top:1.1rem; margin-top:1.5rem; }
div[data-testid="stSidebar"] { background:#0e1629; border-right:1px solid rgba(255,255,255,.08); }
.hub-title { padding:.75rem .8rem 1rem; margin:0 -.35rem .7rem; border:1px solid rgba(255,255,255,.09); border-radius:18px; background:linear-gradient(135deg, rgba(25,36,64,.96), rgba(14,22,41,.98)); box-shadow:0 12px 28px rgba(0,0,0,.22); position:relative; overflow:hidden; min-height:112px; }
.hub-title:before { content:''; position:absolute; width:112px; height:112px; right:-28px; top:0; border:1px solid rgba(255,204,102,.12); border-radius:50%; animation: hub-orbit 12s linear infinite; }
.hub-candy-field { position:absolute; inset:0; pointer-events:none; opacity:.72; transition:opacity .25s ease; }
.hub-candy { position:absolute; width:16px; height:16px; border-radius:50%; background:radial-gradient(circle at 32% 27%, rgba(255,255,255,.42) 0 9%, transparent 10%), linear-gradient(135deg, rgba(255,204,102,.78), rgba(255,120,145,.50) 48%, rgba(155,140,255,.60)); box-shadow:0 0 13px rgba(255,204,102,.18), inset -3px -4px 6px rgba(0,0,0,.25); opacity:.62; animation: candy-float 7s ease-in-out infinite alternate; transition:opacity .25s ease, filter .25s ease; }
.hub-candy:before, .hub-candy:after { content:''; position:absolute; top:4px; width:8px; height:9px; background:rgba(255,204,102,.36); filter:blur(.4px); }
.hub-candy:before { left:-6px; clip-path:polygon(100% 20%, 0 0, 30% 50%, 0 100%, 100% 80%); }
.hub-candy:after { right:-6px; clip-path:polygon(0 20%, 100% 0, 70% 50%, 100% 100%, 0 80%); }
.hub-candy.c1 { left:8%; top:16%; animation-delay:-1s; transform:scale(.72); }
.hub-candy.c2 { left:26%; top:68%; animation-delay:-3s; transform:scale(.55); }
.hub-candy.c3 { left:48%; top:18%; animation-delay:-5s; transform:scale(.48); }
.hub-candy.c4 { left:68%; top:70%; animation-delay:-2s; transform:scale(.68); }
.hub-candy.c5 { right:8%; top:14%; animation-delay:-6s; transform:scale(.82); }
.hub-candy.c6 { right:22%; bottom:8%; animation-delay:-4s; transform:scale(.42); }
.hub-title:hover .hub-candy-field { opacity:1; }
.hub-title:hover .hub-candy { animation-duration:1.9s; filter:brightness(1.3) drop-shadow(0 0 7px rgba(255,204,102,.35)); opacity:.92; }
.hub-title > *:not(.hub-candy-field) { position:relative; z-index:1; }
@keyframes hub-orbit { from { transform:rotate(0deg); } to { transform:rotate(360deg); } }
@keyframes candy-float { from { margin-left:-7px; margin-top:5px; rotate:-12deg; } to { margin-left:10px; margin-top:-6px; rotate:16deg; } }
.hub-kicker { color:var(--cyan); font-size:.68rem; text-transform:uppercase; letter-spacing:.16em; font-weight:700; }
.hub-name { color:var(--ink); font-family:'Space Grotesk', sans-serif; font-size:1.18rem; line-height:1.15; font-weight:700; margin-top:.25rem; }
.stDataFrame { border-radius:14px; overflow:hidden; }
.stTabs [data-baseweb="tab-list"] { gap:1.2rem; }
.stTabs [data-baseweb="tab"] { color:var(--muted); }
.stTabs [aria-selected="true"] { color:var(--accent) !important; }
[data-testid="stMetricValue"] { color:var(--ink); }
</style>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_dataset():
    return clean_data(ROOT / "data" / "NassauCandyDistributor.csv")

def money(x): return f"${x:,.0f}"
def pct(x): return f"{x:,.1f}%"
def no_data(message="No products match the selected criteria."):
    st.info(message)

def plot_layout(fig, height=370):
    fig.update_layout(height=height, template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,29,51,.65)", margin=dict(l=10,r=10,t=40,b=10), font=dict(color="#eef3ff"), legend=dict(orientation="h", y=1.1))
    return fig

df, stats = load_dataset()
prod_all = aggregate_products(df)
div_all = aggregate_divisions(df)

st.markdown('<div class="hero"><div class="eyebrow">Executive profitability intelligence</div><h1>Product Line Profitability & Margin Performance</h1><p class="subtle">Nassau Candy Distributor · A filter-aware view of profit drivers, margin risk, concentration, and factory performance.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="hub-title"><div class="hub-candy-field" aria-hidden="true"><span class="hub-candy c1"></span><span class="hub-candy c2"></span><span class="hub-candy c3"></span><span class="hub-candy c4"></span><span class="hub-candy c5"></span><span class="hub-candy c6"></span></div><div class="hub-kicker">Nassau Candy Distributor</div><div class="hub-name">Profitability<br>Intelligence Hub</div></div>', unsafe_allow_html=True)
    st.caption(f"Source: {stats['clean_rows']:,} validated rows")
    min_date, max_date = df["Order Date"].min().date(), df["Order Date"].max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    else:
        start_date, end_date = pd.Timestamp(min_date), pd.Timestamp(max_date)
    divisions = st.multiselect("Division", sorted(df["Division"].dropna().unique()), default=sorted(df["Division"].dropna().unique()))
    regions = st.multiselect("Region", sorted(df["Region"].dropna().unique()), default=sorted(df["Region"].dropna().unique()))
    factory_choices = sorted(df["Factory"].dropna().unique())
    factories = st.multiselect("Factory", factory_choices, default=factory_choices)
    margin_threshold = st.slider("Minimum gross margin (%)", 0.0, 100.0, 0.0, 1.0)
    product_search = st.text_input("Search product", placeholder="e.g. Wonka, Taffy")
    st.markdown("---")
    st.caption("All metrics recalculate from the uploaded dataset. No demo or synthetic rows are used.")

mask = (df["Order Date"].between(start_date, end_date) & df["Division"].isin(divisions) & df["Region"].isin(regions) & df["Factory"].isin(factories))
filtered = df.loc[mask].copy()
products = aggregate_products(filtered)
if product_search:
    products = products[products["Product Name"].str.contains(product_search, case=False, na=False)].copy()
products = products[products["Gross Margin %"] >= margin_threshold].copy()
divisions_df = aggregate_divisions(filtered)

st.markdown('<div class="section"><div class="eyebrow">01 · Executive overview</div><h2>Portfolio pulse</h2></div>', unsafe_allow_html=True)
total_sales, total_profit, total_units = filtered["Sales"].sum(), filtered["Gross Profit"].sum(), filtered["Units"].sum()
avg_margin = total_profit / total_sales * 100 if total_sales else 0
profit_pareto = pareto(filtered, "Gross Profit")
profit_80 = int((profit_pareto["Cumulative %"] <= 80).sum() + (1 if not profit_pareto.empty and (profit_pareto["Cumulative %"] <= 80).sum() < len(profit_pareto) else 0))
kpis = [("Total sales", money(total_sales), f"{len(filtered):,} rows"), ("Gross profit", money(total_profit), f"{avg_margin:.1f}% blended margin"), ("Total units", f"{total_units:,.0f}", f"{filtered['Product Name'].nunique()} products"), ("Profit concentration", f"{profit_80}/{max(len(profit_pareto),1)}", "products to reach ~80% profit"), ("Divisions", f"{filtered['Division'].nunique()}", "active in selection")]
cols = st.columns(len(kpis))
for c, (label, value, note) in zip(cols, kpis):
    c.markdown(f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>', unsafe_allow_html=True)

if filtered.empty:
    no_data()
else:
    insight = products.iloc[0] if not products.empty else aggregate_products(filtered).iloc[0]
    st.markdown(f"**Current read:** {insight['Product Name']} leads the selected portfolio on gross profit at **{money(insight['Gross Profit'])}**. Use the tabs below to distinguish scale from margin quality and concentration.")

with st.container():
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Product profitability", "Division performance", "Cost diagnostics", "Profit concentration", "Factory analysis"])
    with tab1:
        st.markdown("### Product margin leaderboard")
        if products.empty: no_data()
        else:
            left, right = st.columns(2)
            top_profit = products.sort_values("Gross Profit", ascending=False).head(10).sort_values("Gross Profit")
            fig = px.bar(top_profit, x="Gross Profit", y="Product Name", color="Gross Margin %", color_continuous_scale="Viridis", orientation="h", title="Top products by gross profit", hover_data=["Sales","Gross Margin %","Profit per Unit"])
            left.plotly_chart(plot_layout(fig), use_container_width=True)
            top_margin = products.sort_values("Gross Margin %", ascending=False).head(10).sort_values("Gross Margin %")
            fig2 = px.bar(top_margin, x="Gross Margin %", y="Product Name", color="Gross Profit", color_continuous_scale="Sunset", orientation="h", title="Highest-margin products", hover_data=["Sales","Gross Profit"])
            right.plotly_chart(plot_layout(fig2), use_container_width=True)
            display = products[["Product Name","Division","Factory","Sales","Gross Profit","Gross Margin %","Profit per Unit","Revenue Contribution %","Profit Contribution %","Margin Risk","Diagnostic"]].copy()
            st.dataframe(display.style.format({"Sales":"${:,.2f}","Gross Profit":"${:,.2f}","Gross Margin %":"{:.1f}%","Profit per Unit":"${:,.2f}","Revenue Contribution %":"{:.1f}%","Profit Contribution %":"{:.1f}%"}), use_container_width=True, hide_index=True)

    with tab2:
        st.markdown("### Division performance")
        if divisions_df.empty: no_data()
        else:
            left, right = st.columns(2)
            melt = divisions_df.melt(id_vars="Division", value_vars=["Sales","Gross Profit"], var_name="Metric", value_name="Value")
            fig = px.bar(melt, x="Division", y="Value", color="Metric", barmode="group", title="Revenue versus gross profit", color_discrete_sequence=["#5de2e7","#ffcc66"])
            left.plotly_chart(plot_layout(fig), use_container_width=True)
            fig2 = px.bar(divisions_df, x="Division", y="Gross Margin %", color="Division", title="Gross margin by division", color_discrete_sequence=["#9b8cff","#5de2e7","#ff7891"])
            right.plotly_chart(plot_layout(fig2), use_container_width=True)
            st.dataframe(divisions_df.style.format({"Sales":"${:,.2f}","Cost":"${:,.2f}","Gross Profit":"${:,.2f}","Gross Margin %":"{:.1f}%","Profit per Unit":"${:,.2f}","Revenue Contribution %":"{:.1f}%","Profit Contribution %":"{:.1f}%"}), use_container_width=True, hide_index=True)

    with tab3:
        st.markdown("### Cost versus margin diagnostics")
        if products.empty: no_data()
        else:
            left, right = st.columns(2)
            fig = px.scatter(products, x="Sales", y="Cost", size="Gross Profit", color="Gross Margin %", hover_name="Product Name", color_continuous_scale="Turbo", title="Sales versus cost")
            left.plotly_chart(plot_layout(fig), use_container_width=True)
            fig2 = px.scatter(products, x="Cost", y="Gross Margin %", size="Sales", color="Margin Risk", hover_name="Product Name", title="Cost versus margin risk", color_discrete_sequence=["#ff7891","#ffcc66","#5de2e7","#9b8cff"])
            right.plotly_chart(plot_layout(fig2), use_container_width=True)
            risk = products[(products["Margin Risk"] != "High profit / high margin") | (products["Gross Margin %"] < margin_threshold + 10)].copy()
            if risk.empty: risk = products.copy()
            st.dataframe(risk[["Product Name","Division","Sales","Cost","Gross Profit","Gross Margin %","Margin Risk","Diagnostic"]].style.format({"Sales":"${:,.2f}","Cost":"${:,.2f}","Gross Profit":"${:,.2f}","Gross Margin %":"{:.1f}%"}), use_container_width=True, hide_index=True)

    with tab4:
        st.markdown("### Pareto concentration")
        if filtered.empty: no_data()
        else:
            rev, prof = pareto(filtered, "Sales"), pareto(filtered, "Gross Profit")
            left, right = st.columns(2)
            fig = go.Figure()
            fig.add_trace(go.Bar(x=rev["Product Name"], y=rev["Sales"], name="Sales", marker_color="#5de2e7"))
            fig.add_trace(go.Scatter(x=rev["Product Name"], y=rev["Cumulative %"], name="Cumulative %", yaxis="y2", line=dict(color="#ffcc66", width=3)))
            fig.update_layout(title="Revenue Pareto", yaxis=dict(title="Sales"), yaxis2=dict(title="Cumulative %", overlaying="y", side="right", range=[0,105]))
            left.plotly_chart(plot_layout(fig), use_container_width=True)
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(x=prof["Product Name"], y=prof["Gross Profit"], name="Gross profit", marker_color="#9b8cff"))
            fig2.add_trace(go.Scatter(x=prof["Product Name"], y=prof["Cumulative %"], name="Cumulative %", yaxis="y2", line=dict(color="#ffcc66", width=3)))
            fig2.update_layout(title="Profit Pareto", yaxis=dict(title="Gross profit"), yaxis2=dict(title="Cumulative %", overlaying="y", side="right", range=[0,105]))
            right.plotly_chart(plot_layout(fig2), use_container_width=True)
            rev80 = int((rev["Cumulative %"] <= 80).sum() + (1 if not rev.empty and (rev["Cumulative %"] <= 80).sum() < len(rev) else 0))
            prof80 = int((prof["Cumulative %"] <= 80).sum() + (1 if not prof.empty and (prof["Cumulative %"] <= 80).sum() < len(prof) else 0))
            c1,c2,c3 = st.columns(3)
            c1.metric("Products to ~80% revenue", f"{rev80}/{len(rev)}")
            c2.metric("Products to ~80% profit", f"{prof80}/{len(prof)}")
            c3.metric("Profit dependency ratio", f"{prof80/max(len(prof),1)*100:.1f}%")

    with tab5:
        st.markdown("### Factory and product analysis")
        if filtered.empty: no_data()
        else:
            fs = factory_summary(filtered)
            left, right = st.columns([1.1, 1])
            fig = px.scatter(fs, x="Sales", y="Gross Profit", size="Units", color="Gross Margin %", text="Factory", title="Factory scale and profit", color_continuous_scale="Viridis")
            fig.update_traces(textposition="top center")
            left.plotly_chart(plot_layout(fig), use_container_width=True)
            st.dataframe(fs.style.format({"Sales":"${:,.2f}","Cost":"${:,.2f}","Gross Profit":"${:,.2f}","Gross Margin %":"{:.1f}%"}), use_container_width=True, hide_index=True)
            mapping = pd.DataFrame([{"Factory":f,"Latitude":v["Latitude"],"Longitude":v["Longitude"],"Products":", ".join(sorted([p for p,ff in PRODUCT_FACTORY.items() if ff==f]))} for f,v in FACTORIES.items()])
            st.markdown("#### Factory locations and product mapping")
            st.dataframe(mapping, use_container_width=True, hide_index=True)
            st.map(mapping.rename(columns={"Latitude":"lat","Longitude":"lon"})[["lat","lon"]], zoom=3)

st.markdown('<div class="section"><div class="eyebrow">Data quality</div><h2>Validation checks</h2></div>', unsafe_allow_html=True)
st.caption("These checks describe what happened when the uploaded CSV was prepared for analysis. A zero in the removal checks is positive: it means the source rows already passed that rule.")
with st.expander("Show validation evidence"):
    check_table = validation_report(df, stats).copy()
    check_table["Status"] = np.where(check_table["Passed"], "PASS", "REVIEW")
    st.dataframe(check_table[["Status", "Check", "Evidence"]], use_container_width=True, hide_index=True)
    st.markdown("#### Preparation summary")
    summary_rows = pd.DataFrame([
        {"Measure": "Raw rows", "Value": f"{stats['raw_rows']:,}", "Meaning": "Rows read from the uploaded CSV."},
        {"Measure": "Clean rows", "Value": f"{stats['clean_rows']:,}", "Meaning": "Rows available to the dashboard after validation."},
        {"Measure": "Removed rows", "Value": f"{stats['removed_rows']:,}", "Meaning": "Rows excluded for invalid data or duplicate records."},
        {"Measure": "Duplicate rows detected", "Value": f"{stats['duplicate_rows']:,}", "Meaning": "Exact duplicate rows found in the source."},
        {"Measure": "Invalid rows detected", "Value": f"{stats['invalid_rows']:,}", "Meaning": "Rows with missing dates, invalid numeric values, or non-positive sales/units."},
        {"Measure": "Missing values after cleaning", "Value": f"{stats['missing_values_after_cleaning']:,}", "Meaning": "Blank values remaining in the cleaned analytical frame."},
    ])
    st.dataframe(summary_rows, use_container_width=True, hide_index=True)

st.caption("Built for Nassau Candy Distributor · Calculations use only the uploaded NassauCandyDistributor.csv file.")
