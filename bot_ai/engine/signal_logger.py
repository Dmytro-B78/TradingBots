# ================================================================
# NT-Tech SignalLogger 2.0
# Stores last strategy outputs for debug
# ASCII-only, deterministic, no Cyrillic
# ================================================================

class SignalLogger:
    def __init__(self):
        self.last_strategy_outputs = []
        self.last_decision = None
        self.last_regime = None

    def log(self, candle, regime, total_conf, decision, strategy_signals):
        # strategy_signals is a list of tuples: (name, signal, confidence)
        # we store only (name, signal)
        self.last_strategy_outputs = [(name, sig) for (name, sig, conf) in strategy_signals]

        self.last_decision = decision
        self.last_regime = regime
