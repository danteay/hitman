"""Load project configuration"""

import pathlib
import yaml


def load():
    """
    Load local config yml file
    :return: (dict)
    """

    path = pathlib.Path(__file__).parent.absolute()
    file = f"{path}/config.yml"

    config = open(file)

    data = yaml.load(config, Loader=yaml.FullLoader)

    return data


CONFIG = load()
