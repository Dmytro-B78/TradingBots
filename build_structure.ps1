New-Item -ItemType Directory -Path "C:\TradingBots\NT" -Force | Out-Null
New-Item -ItemType Directory -Path "C:\TradingBots\NT\bot_ai" -Force | Out-Null
New-Item -ItemType Directory -Path "C:\TradingBots\NT\bot_ai\config" -Force | Out-Null
New-Item -ItemType Directory -Path "C:\TradingBots\NT\bot_ai\engine" -Force | Out-Null
New-Item -ItemType Directory -Path "C:\TradingBots\NT\bot_ai\strategy" -Force | Out-Null
New-Item -ItemType Directory -Path "C:\TradingBots\NT\scripts" -Force | Out-Null

New-Item -ItemType File -Path "C:\TradingBots\NT\main.py" -Force | Out-Null
New-Item -ItemType File -Path "C:\TradingBots\NT\config.json" -Force | Out-Null
New-Item -ItemType File -Path "C:\TradingBots\NT\README.md" -Force | Out-Null
New-Item -ItemType File -Path "C:\TradingBots\NT\CHANGELOG.md" -Force | Out-Null

New-Item -ItemType File -Path "C:\TradingBots\NT\bot_ai\config\config.py" -Force | Out-Null

New-Item -ItemType File -Path "C:\TradingBots\NT\bot_ai\engine\backtest_engine.py" -Force | Out-Null
New-Item -ItemType File -Path "C:\TradingBots\NT\bot_ai\engine\live_engine.py" -Force | Out-Null
New-Item -ItemType File -Path "C:\TradingBots\NT\bot_ai\engine\data_loader.py" -Force | Out-Null
New-Item -ItemType File -Path "C:\TradingBots\NT\bot_ai\engine\file_logger.py" -Force | Out-Null
New-Item -ItemType File -Path "C:\TradingBots\NT\bot_ai\engine\utils.py" -Force | Out-Null
New-Item -ItemType File -Path "C:\TradingBots\NT\bot_ai\engine\risk_manager.py" -Force | Out-Null
New-Item -ItemType File -Path "C:\TradingBots\NT\bot_ai\engine\strategy_router.py" -Force | Out-Null
New-Item -ItemType File -Path "C:\TradingBots\NT\bot_ai\engine\config_loader.py" -Force | Out-Null
New-Item -ItemType File -Path "C:\TradingBots\NT\bot_ai\engine\trade_analyzer.py" -Force | Out-Null

New-Item -ItemType File -Path "C:\TradingBots\NT\bot_ai\strategy\meta_strategy.py" -Force | Out-Null
New-Item -ItemType File -Path "C:\TradingBots\NT\bot_ai\strategy\ma_crossover_strategy.py" -Force | Out-Null
New-Item -ItemType File -Path "C:\TradingBots\NT\bot_ai\strategy\rsi_strategy.py" -Force | Out-Null
New-Item -ItemType File -Path "C:\TradingBots\NT\bot_ai\strategy\macd_strategy.py" -Force | Out-Null
New-Item -ItemType File -Path "C:\TradingBots\NT\bot_ai\strategy\bollinger_strategy.py" -Force | Out-Null

New-Item -ItemType File -Path "C:\TradingBots\NT\scripts\run_live.ps1" -Force | Out-Null
New-Item -ItemType File -Path "C:\TradingBots\NT\scripts\run_dry.ps1" -Force | Out-Null
New-Item -ItemType File -Path "C:\TradingBots\NT\scripts\run_backtest.ps1" -Force | Out-Null
