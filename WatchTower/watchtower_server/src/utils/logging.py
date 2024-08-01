import logging

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/server.log")
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
