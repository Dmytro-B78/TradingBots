import json
import os

import pandas as pd
import plotly.express as px
import streamlit as st

from bot_ai.risk.report import RiskReport

# === Р вЂ”Р В°Р С–РЎР‚РЎС“Р В¶Р В°Р ВµР С Р С”Р С•Р Р…РЎвЂћР С‘Р С– ===
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
st.title(f"?? {bot_name} ({bot_short}) РІР‚вЂќ РЎР‚Р ВµР В¶Р С‘Р С: {bot_mode}")

# === Р вЂ™Р С”Р В»Р В°Р Т‘Р С”Р С‘ ===
tab1, tab2, tab3 = st.tabs(
    ["?? Р ВРЎРѓРЎвЂљР С•РЎР‚Р С‘РЎРЏ РЎРѓР Т‘Р ВµР В»Р С•Р С”", "?? Equity Curve", "??? RiskGuard"])

with tab1:
    st.header("Р ВРЎРѓРЎвЂљР С•РЎР‚Р С‘РЎРЏ РЎРѓР Т‘Р ВµР В»Р С•Р С” (live/dry-run)")
    trades_file = "data/trades_log.csv"
    if os.path.exists(trades_file) and os.path.getsize(trades_file) > 0:
        df_trades = pd.read_csv(trades_file)

        # Р В¤Р С‘Р В»РЎРЉРЎвЂљРЎР‚РЎвЂ№
        symbol_filter = st.selectbox(
            "Р В¤Р С‘Р В»РЎРЉРЎвЂљРЎР‚ Р С—Р С• Р С—Р В°РЎР‚Р Вµ",
            ["Р вЂ™РЎРѓР Вµ"] +
            sorted(
                df_trades["Symbol"].dropna().unique().tolist()))
        side_filter = st.selectbox(
            "Р В¤Р С‘Р В»РЎРЉРЎвЂљРЎР‚ Р С—Р С• Р Р…Р В°Р С—РЎР‚Р В°Р Р†Р В»Р ВµР Р…Р С‘РЎР‹", [
                "Р вЂ™РЎРѓР Вµ", "BUY", "SELL"])
        if symbol_filter != "Р вЂ™РЎРѓР Вµ":
            df_trades = df_trades[df_trades["Symbol"] == symbol_filter]
        if side_filter != "Р вЂ™РЎРѓР Вµ":
            df_trades = df_trades[df_trades["Side"].str.upper() == side_filter]

        st.dataframe(
            df_trades.sort_values(
                "Time",
                ascending=False),
            use_container_width=True)

        # Р РЋРЎвЂљР В°РЎвЂљР С‘РЎРѓРЎвЂљР С‘Р С”Р В°
        closed_trades = df_trades.dropna(subset=["Profit(%)"])
        total_trades = len(df_trades)
        total_closed = len(closed_trades)
        profitable = len(closed_trades[closed_trades["Profit(%)"] > 0])
        total_profit_pct = closed_trades["Profit(%)"].sum()
        total_profit_usdt = closed_trades["Profit(USDT)"].sum()

        st.markdown(f"**Р вЂ™РЎРѓР ВµР С–Р С• РЎРѓР Т‘Р ВµР В»Р С•Р С”:** {total_trades}")
        st.markdown(f"**Р вЂ”Р В°Р С”РЎР‚РЎвЂ№РЎвЂљРЎвЂ№РЎвЂ¦ РЎРѓР Т‘Р ВµР В»Р С•Р С”:** {total_closed}")
        st.markdown(
            f"**Р СџРЎР‚Р С‘Р В±РЎвЂ№Р В»РЎРЉР Р…РЎвЂ№РЎвЂ¦ РЎРѓР Т‘Р ВµР В»Р С•Р С”:** {profitable} ({(profitable / total_closed * 100 if total_closed else 0):.1f}%)")
        st.markdown(
            f"**Р РЋРЎС“Р СР СР В°РЎР‚Р Р…Р В°РЎРЏ Р С—РЎР‚Р С‘Р В±РЎвЂ№Р В»РЎРЉ:** {total_profit_pct:.2f}% / {total_profit_usdt:.2f} USDT")

    else:
        st.info("Р В¤Р В°Р в„–Р В» trades_log.csv Р С—Р С•Р С”Р В° Р Р…Р Вµ РЎРѓР С•Р В·Р Т‘Р В°Р Р… Р С‘Р В»Р С‘ Р С—РЎС“РЎРѓРЎвЂљ.")

with tab2:
    st.header("Equity Curve")
    trades_file = "data/trades_log.csv"
    if os.path.exists(trades_file) and os.path.getsize(trades_file) > 0:
        df_trades = pd.read_csv(trades_file)
        equity = 1000  # РЎРѓРЎвЂљР В°РЎР‚РЎвЂљР С•Р Р†РЎвЂ№Р в„– Р Т‘Р ВµР С—Р С•Р В·Р С‘РЎвЂљ
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
        st.info("Р СњР ВµРЎвЂљ Р Т‘Р В°Р Р…Р Р…РЎвЂ№РЎвЂ¦ Р Т‘Р В»РЎРЏ Р С—Р С•РЎРѓРЎвЂљРЎР‚Р С•Р ВµР Р…Р С‘РЎРЏ Р С–РЎР‚Р В°РЎвЂћР С‘Р С”Р В°.")

with tab3:
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
    else:
        st.info("Р В¤Р В°Р в„–Р В»РЎвЂ№ risk_log.csv Р С‘ risk_pass_log.csv Р С—Р С•Р С”Р В° Р Р…Р Вµ РЎРѓР С•Р В·Р Т‘Р В°Р Р…РЎвЂ№.")


