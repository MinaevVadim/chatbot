import datetime
import os
import pathlib
import sys

import numpy as np
import matplotlib.pyplot
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.getcwd()))
from chatbot_logger import add_logger, decorator_main_logger

PATH = pathlib.Path(__file__).parent / "files"
matplotlib.pyplot.set_loglevel(level="warning")

logger = add_logger(__name__)


@decorator_main_logger(logger)
async def get_diagram(idd: int, habits: list[dict[str]]) -> str:
    """Displaying statistics on completed habits in the form of a chart"""
    name_habits = [i["name_habit"] for i in habits]
    current_count = [i["count"] for i in habits]
    target_count = [21 - i["count"] for i in habits]
    sex_counts = {
        "current": np.array(current_count),
        "target": np.array(target_count),
    }
    width = 0.6
    fig, ax = plt.subplots()
    bottom = np.zeros(len(name_habits))
    for sex, sex_count in sex_counts.items():
        p = ax.bar(name_habits, sex_count, width, label=sex, bottom=bottom)
        bottom += sex_count
        ax.bar_label(p, label_type="center")
    month = datetime.datetime.now().strftime("%B")
    ax.set(ylabel="Count of habits", xlabel="Habits", title=month)
    ax.legend()
    path = f"{PATH}/diagram{idd}.png"
    plt.savefig(path)
    return path
