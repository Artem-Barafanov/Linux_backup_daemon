import os
import time
import json
import shutil
import logging
import tarfile
from datetime import datetime

CONFIG_FILE = "/etc/backup_daemon.conf"

def load_config():
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {CONFIG_FILE}")
        raise
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in configuration file: {CONFIG_FILE}")
        raise

def backup(config):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(config["backup_dir"], f"backup_{timestamp}.tar.gz")

        # Создаем архив .tar.gz
        with tarfile.open(backup_file, "w:gz") as tar:
            tar.add(config["source_dir"], arcname=os.path.basename(config["source_dir"]))

        logging.info(f"Backup created: {backup_file}")
    except Exception as e:
        logging.error(f"Backup failed: {e}")

def main():
    try:
        config = load_config()
        logging.basicConfig(filename=config["log_file"], level=logging.INFO)

        while True:
            backup(config)
            time.sleep(config["interval_seconds"])
    except Exception as e:
        logging.error(f"Daemon failed: {e}")

if __name__ == "__main__":
    main()