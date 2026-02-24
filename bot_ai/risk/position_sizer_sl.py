class PositionSizerWithSL:
    def __init__(self, config):
        self.config = config

    def calculate_size(self, balance, price, sl):
        risk_amount = balance * self.config.risk.risk_per_trade
        if sl <= 0:
            return 0
        size = risk_amount / sl
        return size

