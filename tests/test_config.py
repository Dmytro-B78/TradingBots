import pytest
import json
from bot_ai.core import config

def test_load_valid_config(tmp_path):
    cfg_file = tmp_path / "cfg.json"
    cfg_file.write_text(json.dumps({
        "risk": {"min_24h_volume_usdt": 2000000},
        "sl_tp": {"sl_type": "fixed", "sl_value": 1.5},
        "pair_selection": {"d1_timeframe": "4h"}
    }))
    cfg = config.load_config(cfg_file)
    assert cfg.risk.min_24h_volume_usdt == 2000000
    assert cfg.sl_tp.sl_type == "fixed"
    assert cfg.pair_selection.d1_timeframe == "4h"

def test_missing_key_defaults(tmp_path):
    cfg_file = tmp_path / "cfg.json"
    cfg_file.write_text(json.dumps({}))
    cfg = config.load_config(cfg_file)
    assert cfg.risk.max_positions == 3
    assert cfg.sl_tp.tp_value == 3.0
    assert cfg.pair_selection.ltf_sma_fast == 20

def test_file_not_found(tmp_path):
    missing_file = tmp_path / "no_config.json"
    with pytest.raises(FileNotFoundError):
        config.load_config(missing_file)
