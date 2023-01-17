import shutil
from pathlib import Path
from my_logging import logger
import yaml


def move_file(original_file_path, new_file_path):
    original_file = Path(original_file_path)
    new_file = Path(new_file_path)
    if not original_file.exists():
        logger.error("The orginal file does not exist {}".format(original_file_path))
    elif new_file.exists():
        logger.error("The destination file already exists {}".format(new_file_path))
    else:
        dest = shutil.move(original_file, new_file)
        return dest
    return None


def write_dict_to_yaml(data, open_type, file_name):
    if not data or not file_name:
        logger.error("Unable to process {} into file: {}".format(data, file_name))
        return None
    with open(file_name, open_type) as f:
        # width paramater should stop it from splitting long lines
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, width=1000)
