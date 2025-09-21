import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime
from bot_ai.risk.report import RiskReport

def plot_riskguard_heatmap(log_file: str = "risk_log.csv"):
    """Строит тепловую карту отказов RiskGuard по дням и часам"""
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
        title="Heatmap отказов RiskGuard (по дням и часам)"
    )
    return fig


def show_riskguard_tab():
    st.header("🛡️ RiskGuard — статистика отказов и успешных сделок")
    deny_file = "risk_log.csv"
    pass_file = "risk_pass_log.csv"

    if os.path.exists(deny_file) or os.path.exists(pass_file):
        report = RiskReport(deny_file, pass_file)
        summary = report.generate_summary()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Всего сделок", summary["total_trades"])
        col2.metric("Разрешено", summary["total_passes"])
        col3.metric("Отказано", summary["total_denies"])
        col4.metric("Успешность", f"{summary['success_rate_pct']:.1f}%")

        # Pie chart причин отказов
        if summary["denies_by_reason"]:
            df_reasons = pd.DataFrame(list(summary["denies_by_reason"].items()), columns=["Причина", "Количество"])
            fig = px.pie(df_reasons, names="Причина", values="Количество", title="Причины отказов")
            st.plotly_chart(fig, use_container_width=True)

        # Линия динамики отказов по времени
        if os.path.exists(deny_file):
            df_denies = pd.read_csv(deny_file)
            if not df_denies.empty:
                fig2 = px.line(df_denies, x="timestamp", y=df_denies.index, title="Динамика отказов", markers=True)
                st.plotly_chart(fig2, use_container_width=True)

        # Heatmap по дням и часам
        fig_heatmap = plot_riskguard_heatmap(deny_file)
        if fig_heatmap:
            st.plotly_chart(fig_heatmap, use_container_width=True)

        # === Экспорт отчёта ===
        if st.button("💾 Сохранить отчёт (HTML)"):
            html_report = f"""
            <html>
            <head><meta charset="utf-8"><title>RiskGuard Report</title></head>
            <body>
            <h1>📊 RiskGuard Report — {datetime.now().strftime("%Y-%m-%d")}</h1>
            <p><b>Всего сделок:</b> {summary['total_trades']}</p>
            <p><b>Разрешено:</b> {summary['total_passes']}</p>
            <p><b>Отказано:</b> {summary['total_denies']}</p>
            <p><b>Успешность:</b> {summary['success_rate_pct']:.1f}%</p>
            <h2>Причины отказов</h2>
            <ul>
            {''.join([f"<li>{reason}: {count}</li>" for reason, count in summary['denies_by_reason'].items()])}
            </ul>
            </body>
            </html>
            """
            reports_dir = "reports"
            os.makedirs(reports_dir, exist_ok=True)
            file_path = os.path.join(reports_dir, f"risk_report_{datetime.now().strftime('%Y%m%d')}.html")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_report)
            st.success(f"Отчёт сохранён: {file_path}")

    else:
        st.info("Файлы risk_log.csv и risk_pass_log.csv пока не созданы.")
