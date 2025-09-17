import logging

def setup_logging(level='INFO', log_file=None):
    logger = logging.getLogger()
    logger.setLevel(level.upper())

    # Формат логов
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    # Вывод в консоль
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Запись в файл, если указан
    if log_file:
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
