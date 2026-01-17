# === bot_ai/dashboard.py ===
# Streamlit Dashboard для анализа сделок и RiskGuard
# Обновлено: добавлена поддержка фильтрации сделок с Side = FLAT

import json
import os

import pandas as pd
import plotly.express as px
import streamlit as st

from bot_ai.risk.report import RiskReport

# === Загружаем конфиг ===
CONFIG_PATH = "config.json"
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    bot_name = cfg.get("bot_name", "TradingBot")
    bot_short = cfg.get("bot_short", "")
    bot_mode = cfg.get("mode", "unknown")
else:
    bot_name = "TradingBot"
    bot_short = ""
    bot_mode = "unknown"

st.set_page_config(page_title=f"{bot_name} Dashboard", layout="wide")
st.title(f"?? {bot_name} ({bot_short}) — режим: {bot_mode}")

# === Вкладки ===
tab1, tab2, tab3 = st.tabs(
    ["?? История сделок", "?? Equity Curve", "??? RiskGuard"])

with tab1:
    st.header("История сделок (live/dry-run)")
    trades_file = "data/trades_log.csv"
    if os.path.exists(trades_file) and os.path.getsize(trades_file) > 0:
        df_trades = pd.read_csv(trades_file)

        # Фильтры
        symbol_filter = st.selectbox(
            "Фильтр по паре",
            ["Все"] +
            sorted(
                df_trades["Symbol"].dropna().unique().tolist()))
        side_options = ["Все"] + \
            sorted(df_trades["Side"].dropna().unique().tolist())
        side_filter = st.selectbox("Фильтр по направлению", side_options)

        if symbol_filter != "Все":
            df_trades = df_trades[df_trades["Symbol"] == symbol_filter]
        if side_filter != "Все":
            df_trades = df_trades[df_trades["Side"].str.upper(
            ) == side_filter.upper()]

        st.dataframe(
            df_trades.sort_values(
                "Time",
                ascending=False),
            use_container_width=True)

        # Статистика
        closed_trades = df_trades.dropna(subset=["Profit(%)"])
        total_trades = len(df_trades)
        total_closed = len(closed_trades)
        profitable = len(closed_trades[closed_trades["Profit(%)"] > 0])
        total_profit_pct = closed_trades["Profit(%)"].sum()
        total_profit_usdt = closed_trades["Profit(USDT)"].sum()

        st.markdown(f"**Всего сделок:** {total_trades}")
        st.markdown(f"**Закрытых сделок:** {total_closed}")
        st.markdown(
            f"**Прибыльных сделок:** {profitable} ({(profitable / total_closed * 100 if total_closed else 0):.1f}%)")
        st.markdown(
            f"**Суммарная прибыль:** {total_profit_pct:.2f}% / {total_profit_usdt:.2f} USDT")

    else:
        st.info("Файл trades_log.csv пока не создан или пуст.")

with tab2:
    st.header("Equity Curve")
    trades_file = "data/trades_log.csv"
    if os.path.exists(trades_file) and os.path.getsize(trades_file) > 0:
        df_trades = pd.read_csv(trades_file)
        equity = 1000  # стартовый депозит
        equity_curve = []
        for _, row in df_trades.iterrows():
            if not pd.isna(row.get("Profit(USDT)")):
                equity += row["Profit(USDT)"]
            equity_curve.append(equity)
        df_trades["Equity"] = equity_curve
        fig = px.line(
            df_trades,
            x="Time",
            y="Equity",
            title="Equity Curve",
            markers=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Нет данных для построения графика.")

with tab3:
    st.header("??? RiskGuard — статистика отказов и успешных сделок")
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
            df_reasons = pd.DataFrame(
                list(
                    summary["denies_by_reason"].items()),
                columns=[
                    "Причина",
                    "Количество"])
            fig = px.pie(
                df_reasons,
                names="Причина",
                values="Количество",
                title="Причины отказов")
            st.plotly_chart(fig, use_container_width=True)

        # Линия динамики отказов по времени
        if os.path.exists(deny_file):
            df_denies = pd.read_csv(deny_file)
            if not df_denies.empty:
                fig2 = px.line(
                    df_denies,
                    x="timestamp",
                    y=df_denies.index,
                    title="Динамика отказов",
                    markers=True)
                st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Файлы risk_log.csv и risk_pass_log.csv пока не созданы.")

