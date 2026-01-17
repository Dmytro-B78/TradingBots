from pathlib import Path

def save_equity(df, strategy_name):
    """
    Сохраняет DataFrame с кривой капитала в файл results/{strategy_name}_equity.csv
    """
    Path("results").mkdir(exist_ok=True)
    file_path = Path("results") / f"{strategy_name}_equity.csv"
    df.to_csv(file_path, index=False)

