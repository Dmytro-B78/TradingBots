import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from bot_ai.risk.report import RiskReport

# === Р вЂ™Р С”Р В»Р В°Р Т‘Р С”Р С‘ ===
tab3, tab4 = st.tabs(["?? Р вЂњРЎР‚Р В°РЎвЂћР С‘Р С” РЎвЂ Р ВµР Р…РЎвЂ№ РЎРѓ РЎвЂљР С•РЎвЂЎР С”Р В°Р СР С‘ Р Р†РЎвЂ¦Р С•Р Т‘Р В°/Р Р†РЎвЂ№РЎвЂ¦Р С•Р Т‘Р В°", "??? RiskGuard"])

with tab3:
    st.header("Р вЂњРЎР‚Р В°РЎвЂћР С‘Р С” РЎвЂ Р ВµР Р…РЎвЂ№ РЎРѓ РЎвЂљР С•РЎвЂЎР С”Р В°Р СР С‘ Р Р†РЎвЂ¦Р С•Р Т‘Р В°/Р Р†РЎвЂ№РЎвЂ¦Р С•Р Т‘Р В°")

    backtests_dir = "data/backtests"
    if os.path.exists(backtests_dir):
        # Р вЂ™РЎвЂ№Р В±Р С•РЎР‚ РЎвЂљР В°Р в„–Р СРЎвЂћРЎР‚Р ВµР в„–Р СР В°
        timeframe_choice = st.selectbox("Р СћР В°Р в„–Р СРЎвЂћРЎР‚Р ВµР в„–Р С", ["1h", "4h", "1d"])

        # Р вЂ™РЎвЂ№Р В±Р С•РЎР‚ РЎРѓРЎвЂљРЎР‚Р В°РЎвЂљР ВµР С–Р С‘Р в„– Р Т‘Р В»РЎРЏ РЎРѓРЎР‚Р В°Р Р†Р Р…Р ВµР Р…Р С‘РЎРЏ
        strategies = sorted([d for d in os.listdir(
            backtests_dir) if os.path.isdir(os.path.join(backtests_dir, d))])
        col1, col2 = st.columns(2)
        with col1:
            strategy_choice_1 = st.selectbox(
                "Р РЋРЎвЂљРЎР‚Р В°РЎвЂљР ВµР С–Р С‘РЎРЏ 1", strategies, index=0)
        with col2:
            strategy_choice_2 = st.selectbox(
                "Р РЋРЎвЂљРЎР‚Р В°РЎвЂљР ВµР С–Р С‘РЎРЏ 2 (Р С•Р С—РЎвЂ Р С‘Р С•Р Р…Р В°Р В»РЎРЉР Р…Р С•)", ["Р СњР ВµРЎвЂљ"] + strategies, index=0)

        # Р вЂ™РЎвЂ№Р В±Р С•РЎР‚ Р С—Р В°РЎР‚РЎвЂ№
        trades_files_1 = [
            f for f in os.listdir(
                os.path.join(
                    backtests_dir,
                    strategy_choice_1)) if f.endswith("_trades.csv")]
        if trades_files_1:
            pair_choice = st.selectbox("Р вЂ™РЎвЂ№Р В±Р ВµРЎР‚Р С‘ Р С—Р В°РЎР‚РЎС“", trades_files_1)

            fig = go.Figure()

            # Р В¤РЎС“Р Р…Р С”РЎвЂ Р С‘РЎРЏ Р Т‘Р В»РЎРЏ Р Т‘Р С•Р В±Р В°Р Р†Р В»Р ВµР Р…Р С‘РЎРЏ Р Т‘Р В°Р Р…Р Р…РЎвЂ№РЎвЂ¦ РЎРѓРЎвЂљРЎР‚Р В°РЎвЂљР ВµР С–Р С‘Р С‘ Р Р…Р В° Р С–РЎР‚Р В°РЎвЂћР С‘Р С”
            def add_strategy_to_chart(strategy_name, color_buy, color_sell):
                trades_path = os.path.join(
                    backtests_dir, strategy_name, pair_choice)
                trades_df = pd.read_csv(trades_path)

                ohlcv_file = trades_path.replace("_trades.csv", "_ohlcv.csv")
                if os.path.exists(ohlcv_file):
                    ohlcv_df = pd.read_csv(ohlcv_file)
                    ohlcv_df["time"] = pd.to_datetime(
                        ohlcv_df["time"], unit='ms')

                    # Р вЂќР С•Р В±Р В°Р Р†Р В»РЎРЏР ВµР С РЎРѓР Р†Р ВµРЎвЂЎР С‘ РЎвЂљР С•Р В»РЎРЉР С”Р С• Р Т‘Р В»РЎРЏ Р С—Р ВµРЎР‚Р Р†Р С•Р в„– РЎРѓРЎвЂљРЎР‚Р В°РЎвЂљР ВµР С–Р С‘Р С‘
                    if len(fig.data) == 0:
                        fig.add_trace(go.Candlestick(
                            x=ohlcv_df["time"],
                            open=ohlcv_df["open"],
                            high=ohlcv_df["high"],
                            low=ohlcv_df["low"],
                            close=ohlcv_df["close"],
                            name="Р В¦Р ВµР Р…Р В°"
                        ))

                    buys = trades_df[trades_df["Action"] == "BUY"]
                    sells = trades_df[trades_df["Action"] == "SELL"]

                    fig.add_trace(
                        go.Scatter(
                            x=pd.to_datetime(
                                buys["Time"],
                                unit='ms'),
                            y=buys["Price"],
                            mode="markers",
                            marker=dict(
                                symbol="triangle-up",
                                color=color_buy,
                                size=10),
                            name=f"BUY {strategy_name}"))

                    fig.add_trace(
                        go.Scatter(
                            x=pd.to_datetime(
                                sells["Time"],
                                unit='ms'),
                            y=sells["Price"],
                            mode="markers",
                            marker=dict(
                                symbol="triangle-down",
                                color=color_sell,
                                size=10),
                            name=f"SELL {strategy_name}"))

            # Р вЂќР С•Р В±Р В°Р Р†Р В»РЎРЏР ВµР С Р С—Р ВµРЎР‚Р Р†РЎС“РЎР‹ РЎРѓРЎвЂљРЎР‚Р В°РЎвЂљР ВµР С–Р С‘РЎР‹
            add_strategy_to_chart(strategy_choice_1, "green", "red")

            # Р вЂўРЎРѓР В»Р С‘ Р Р†РЎвЂ№Р В±РЎР‚Р В°Р Р…Р В° Р Р†РЎвЂљР С•РЎР‚Р В°РЎРЏ РЎРѓРЎвЂљРЎР‚Р В°РЎвЂљР ВµР С–Р С‘РЎРЏ
            if strategy_choice_2 != "Р СњР ВµРЎвЂљ":
                add_strategy_to_chart(strategy_choice_2, "blue", "orange")

            fig.update_layout(
                title=f"{pair_choice} РІР‚вЂќ РЎРѓРЎР‚Р В°Р Р†Р Р…Р ВµР Р…Р С‘Р Вµ РЎРѓРЎвЂљРЎР‚Р В°РЎвЂљР ВµР С–Р С‘Р в„–",
                xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Р СњР ВµРЎвЂљ РЎвЂћР В°Р в„–Р В»Р С•Р Р† РЎРѓР Т‘Р ВµР В»Р С•Р С” Р Т‘Р В»РЎРЏ Р Р†РЎвЂ№Р В±РЎР‚Р В°Р Р…Р Р…Р С•Р в„– РЎРѓРЎвЂљРЎР‚Р В°РЎвЂљР ВµР С–Р С‘Р С‘.")
    else:
        st.info("Р СџР В°Р С—Р С”Р В° data/backtests Р Р…Р Вµ Р Р…Р В°Р в„–Р Т‘Р ВµР Р…Р В°.")

with tab4:
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


