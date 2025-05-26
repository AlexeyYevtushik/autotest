# filepath: /home/gfjsra/repos/scrap/utils/logger.py
import logging
import os

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)  # Ensure the logs directory exists

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"{log_dir}/app.log"),  # Log to a file
        logging.StreamHandler()                    # Log to the console
    ]
)

logger = logging.getLogger("AppLogger")