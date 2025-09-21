import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px
from bot_ai.risk.report import RiskReport

# === Вкладки ===
tab3, tab4 = st.tabs(["📈 График цены с точками входа/выхода", "🛡️ RiskGuard"])

with tab3:
    st.header("График цены с точками входа/выхода")

    backtests_dir = "data/backtests"
    if os.path.exists(backtests_dir):
        # Выбор таймфрейма
        timeframe_choice = st.selectbox("Таймфрейм", ["1h", "4h", "1d"])

        # Выбор стратегий для сравнения
        strategies = sorted([d for d in os.listdir(backtests_dir) if os.path.isdir(os.path.join(backtests_dir, d))])
        col1, col2 = st.columns(2)
        with col1:
            strategy_choice_1 = st.selectbox("Стратегия 1", strategies, index=0)
        with col2:
            strategy_choice_2 = st.selectbox("Стратегия 2 (опционально)", ["Нет"] + strategies, index=0)

        # Выбор пары
        trades_files_1 = [f for f in os.listdir(os.path.join(backtests_dir, strategy_choice_1)) if f.endswith("_trades.csv")]
        if trades_files_1:
            pair_choice = st.selectbox("Выбери пару", trades_files_1)

            fig = go.Figure()

            # Функция для добавления данных стратегии на график
            def add_strategy_to_chart(strategy_name, color_buy, color_sell):
                trades_path = os.path.join(backtests_dir, strategy_name, pair_choice)
                trades_df = pd.read_csv(trades_path)

                ohlcv_file = trades_path.replace("_trades.csv", "_ohlcv.csv")
                if os.path.exists(ohlcv_file):
                    ohlcv_df = pd.read_csv(ohlcv_file)
                    ohlcv_df["time"] = pd.to_datetime(ohlcv_df["time"], unit='ms')

                    # Добавляем свечи только для первой стратегии
                    if len(fig.data) == 0:
                        fig.add_trace(go.Candlestick(
                            x=ohlcv_df["time"],
                            open=ohlcv_df["open"],
                            high=ohlcv_df["high"],
                            low=ohlcv_df["low"],
                            close=ohlcv_df["close"],
                            name="Цена"
                        ))

                    buys = trades_df[trades_df["Action"] == "BUY"]
                    sells = trades_df[trades_df["Action"] == "SELL"]

                    fig.add_trace(go.Scatter(
                        x=pd.to_datetime(buys["Time"], unit='ms'),
                        y=buys["Price"],
                        mode="markers",
                        marker=dict(symbol="triangle-up", color=color_buy, size=10),
                        name=f"BUY {strategy_name}"
                    ))

                    fig.add_trace(go.Scatter(
                        x=pd.to_datetime(sells["Time"], unit='ms'),
                        y=sells["Price"],
                        mode="markers",
                        marker=dict(symbol="triangle-down", color=color_sell, size=10),
                        name=f"SELL {strategy_name}"
                    ))

            # Добавляем первую стратегию
            add_strategy_to_chart(strategy_choice_1, "green", "red")

            # Если выбрана вторая стратегия
            if strategy_choice_2 != "Нет":
                add_strategy_to_chart(strategy_choice_2, "blue", "orange")

            fig.update_layout(title=f"{pair_choice} — сравнение стратегий", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Нет файлов сделок для выбранной стратегии.")
    else:
        st.info("Папка data/backtests не найдена.")

with tab4:
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
    else:
        st.info("Файлы risk_log.csv и risk_pass_log.csv пока не созданы.")
