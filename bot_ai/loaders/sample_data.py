def load_sample_data():
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    base = 100
    steps = np.cumsum(np.random.randn(100)) + base
    high = steps + np.random.rand(100) * 2
    low = steps - np.random.rand(100) * 2
    open_ = steps + np.random.randn(100) * 0.5
    close = steps
    volume = np.random.randint(1000, 5000, size=100)

    return pd.DataFrame({
        "open": open_,
        "high": high,
        "low": low,
        "close": close,
        "volume": volume
    })

