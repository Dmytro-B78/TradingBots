import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from bot_ai.risk.report import RiskReport

def plot_riskguard_heatmap(log_file: str = "risk_log.csv"):
    """Р РЋРЎвЂљРЎР‚Р С•Р С‘РЎвЂљ РЎвЂљР ВµР С—Р В»Р С•Р Р†РЎС“РЎР‹ Р С”Р В°РЎР‚РЎвЂљРЎС“ Р С•РЎвЂљР С”Р В°Р В·Р С•Р Р† RiskGuard Р С—Р С• Р Т‘Р Р…РЎРЏР С Р С‘ РЎвЂЎР В°РЎРѓР В°Р С"""
    if not os.path.exists(log_file):
        return None
    df = pd.read_csv(log_file)
    if df.empty:
        return None

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["day"] = df["timestamp"].dt.date
    df["hour"] = df["timestamp"].dt.hour

    heatmap_data = df.groupby(["day", "hour"]).size().reset_index(name="count")

    fig = px.density_heatmap(
        heatmap_data,
        x="hour",
        y="day",
        z="count",
        color_continuous_scale="Reds",
        title="Heatmap Р С•РЎвЂљР С”Р В°Р В·Р С•Р Р† RiskGuard (Р С—Р С• Р Т‘Р Р…РЎРЏР С Р С‘ РЎвЂЎР В°РЎРѓР В°Р С)"
    )
    return fig

def show_riskguard_tab():
    st.header("??? RiskGuard РІР‚вЂќ РЎРѓРЎвЂљР В°РЎвЂљР С‘РЎРѓРЎвЂљР С‘Р С”Р В° Р С•РЎвЂљР С”Р В°Р В·Р С•Р Р† Р С‘ РЎС“РЎРѓР С—Р ВµРЎв‚¬Р Р…РЎвЂ№РЎвЂ¦ РЎРѓР Т‘Р ВµР В»Р С•Р С”")
    deny_file = "risk_log.csv"
    pass_file = "risk_pass_log.csv"

    if os.path.exists(deny_file) or os.path.exists(pass_file):
        report = RiskReport(deny_file, pass_file)
        summary = report.generate_summary()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Р вЂ™РЎРѓР ВµР С–Р С• РЎРѓР Т‘Р ВµР В»Р С•Р С”", summary["total_trades"])
        col2.metric("Р В Р В°Р В·РЎР‚Р ВµРЎв‚¬Р ВµР Р…Р С•", summary["total_passes"])
        col3.metric("Р С›РЎвЂљР С”Р В°Р В·Р В°Р Р…Р С•", summary["total_denies"])
        col4.metric("Р Р€РЎРѓР С—Р ВµРЎв‚¬Р Р…Р С•РЎРѓРЎвЂљРЎРЉ", f"{summary['success_rate_pct']:.1f}%")

        # Pie chart Р С—РЎР‚Р С‘РЎвЂЎР С‘Р Р… Р С•РЎвЂљР С”Р В°Р В·Р С•Р Р†
        if summary["denies_by_reason"]:
            df_reasons = pd.DataFrame(
                list(
                    summary["denies_by_reason"].items()),
                columns=[
                    "Р СџРЎР‚Р С‘РЎвЂЎР С‘Р Р…Р В°",
                    "Р С™Р С•Р В»Р С‘РЎвЂЎР ВµРЎРѓРЎвЂљР Р†Р С•"])
            fig = px.pie(
                df_reasons,
                names="Р СџРЎР‚Р С‘РЎвЂЎР С‘Р Р…Р В°",
                values="Р С™Р С•Р В»Р С‘РЎвЂЎР ВµРЎРѓРЎвЂљР Р†Р С•",
                title="Р СџРЎР‚Р С‘РЎвЂЎР С‘Р Р…РЎвЂ№ Р С•РЎвЂљР С”Р В°Р В·Р С•Р Р†")
            st.plotly_chart(fig, use_container_width=True)

        # Р вЂєР С‘Р Р…Р С‘РЎРЏ Р Т‘Р С‘Р Р…Р В°Р СР С‘Р С”Р С‘ Р С•РЎвЂљР С”Р В°Р В·Р С•Р Р† Р С—Р С• Р Р†РЎР‚Р ВµР СР ВµР Р…Р С‘
        if os.path.exists(deny_file):
            df_denies = pd.read_csv(deny_file)
            if not df_denies.empty:
                fig2 = px.line(
                    df_denies,
                    x="timestamp",
                    y=df_denies.index,
                    title="Р вЂќР С‘Р Р…Р В°Р СР С‘Р С”Р В° Р С•РЎвЂљР С”Р В°Р В·Р С•Р Р†",
                    markers=True)
                st.plotly_chart(fig2, use_container_width=True)

        # Heatmap Р С—Р С• Р Т‘Р Р…РЎРЏР С Р С‘ РЎвЂЎР В°РЎРѓР В°Р С
        fig_heatmap = plot_riskguard_heatmap(deny_file)
        if fig_heatmap:
            st.plotly_chart(fig_heatmap, use_container_width=True)

        # === Р В­Р С”РЎРѓР С—Р С•РЎР‚РЎвЂљ Р С•РЎвЂљРЎвЂЎРЎвЂРЎвЂљР В° ===
        if st.button("?? Р РЋР С•РЎвЂ¦РЎР‚Р В°Р Р…Р С‘РЎвЂљРЎРЉ Р С•РЎвЂљРЎвЂЎРЎвЂРЎвЂљ (HTML)"):
            html_report = """
            <html>
            <head><meta charset="utf-8"><title>RiskGuard Report</title></head>
            <body>
            <h1>?? RiskGuard Report РІР‚вЂќ {datetime.now().strftime("%Y-%m-%d")}</h1>
            <p><b>Р вЂ™РЎРѓР ВµР С–Р С• РЎРѓР Т‘Р ВµР В»Р С•Р С”:</b> {summary['total_trades']}</p>
            <p><b>Р В Р В°Р В·РЎР‚Р ВµРЎв‚¬Р ВµР Р…Р С•:</b> {summary['total_passes']}</p>
            <p><b>Р С›РЎвЂљР С”Р В°Р В·Р В°Р Р…Р С•:</b> {summary['total_denies']}</p>
            <p><b>Р Р€РЎРѓР С—Р ВµРЎв‚¬Р Р…Р С•РЎРѓРЎвЂљРЎРЉ:</b> {summary['success_rate_pct']:.1f}%</p>
            <h2>Р СџРЎР‚Р С‘РЎвЂЎР С‘Р Р…РЎвЂ№ Р С•РЎвЂљР С”Р В°Р В·Р С•Р Р†</h2>
            <ul>
            {''.join([f"<li>{reason}: {count}</li>" for reason, count in summary['denies_by_reason'].items()])}
            </ul>
            </body>
            </html>
            """
            reports_dir = "reports"
            os.makedirs(reports_dir, exist_ok=True)
            file_path = os.path.join(
                reports_dir, f"risk_report_{
                    datetime.now().strftime('%Y%m%d')}.html")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_report)
            st.success(f"Р С›РЎвЂљРЎвЂЎРЎвЂРЎвЂљ РЎРѓР С•РЎвЂ¦РЎР‚Р В°Р Р…РЎвЂР Р…: {file_path}")

    else:
        st.info("Р В¤Р В°Р в„–Р В»РЎвЂ№ risk_log.csv Р С‘ risk_pass_log.csv Р С—Р С•Р С”Р В° Р Р…Р Вµ РЎРѓР С•Р В·Р Т‘Р В°Р Р…РЎвЂ№.")


