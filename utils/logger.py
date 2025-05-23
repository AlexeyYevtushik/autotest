# filepath: /home/gfjsra/repos/scrap/utils/logger.py
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),  # Log to a file
        logging.StreamHandler()              # Log to the console
    ]
)

logger = logging.getLogger("AppLogger")