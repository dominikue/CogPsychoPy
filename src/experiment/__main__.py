"""
Experiment for applied cognitive science.

Run from the command line, from the /src directory, with:

`python -m experiment <trials> [-d]`

Examples:
`python -m experiment -d` for running the experiment in debug mode.
`python -m experiment 10` for running only 10 trials.


For more options type 

python -m experiment --help
"""

import sys
import os

import os
import argparse
import yaml

from psychopy import prefs, logging

from experiment.core.experiment import run_experiment
from experiment.utils.conditions import import_conditions
from experiment.utils.config import import_config

# To avoid bug on windows (https://www.psychopy.org/troubleshooting.html#errors-with-getting-setting-the-gamma-ramp)
prefs.general["gammaErrorPolicy"] = "warn"
# Hide pygame prompt
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"


def main(
    debug: bool = False,
):
    """Run the experiment.

    Args:
        debug: (bool) If True, run in debug mode.
    Returns:
        None (psychopy window, data file (.csv, .log, .psydata))
    """

    # Logging settings
    if not debug:
        logging.console.setLevel(logging.EXP)
        log_file_level = logging.INFO
    else:
        logging.console.setLevel(logging.INFO)
        log_file_level = logging.DEBUG
        logging.info("### Debug mode enabled. ###")

    # ----------------------------------------------------------------------------------
    # Import the conditions and configuration from yml files

    # get the folder of the current module
    package_name = os.path.dirname(__file__).split(os.path.sep)[-1]

    # logging.info("package_name: ", package_name)
    conditions = import_conditions(package_name + "/conditions.yml")

    logging.info(conditions)

    config = import_config(
        debug=debug,
        conditions=conditions,
        file_name=package_name + "/config.yml",
    )
    logging.info(config)

    logging.LogFile(
        config.filepath_participant + ".log", level=log_file_level, filemode="w"
    )

    # ----------------------------------------------------------------------------------
    # RUN THE EXPERIMENT
    run_experiment(
        conditions=conditions,
        config=config,
    )
    # ----------------------------------------------------------------------------------


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Command line tool for dithering experiment."
    )
    # parser.add_argument(
    #     "max-trials",
    #     type=int,
    #     nargs="?",  # Make it optional
    #     help="Specify the amount of trials. Default is 100 trials.",
    # )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Pass to enable debug mode (disable fullscreen, increase logging level)",
    )

    args = parser.parse_args()

    main(
        debug=args.debug,
    )
