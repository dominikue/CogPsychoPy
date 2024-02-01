import random
import string
from dataclasses import dataclass
from itertools import product

import yaml
from psychopy import data, logging


@dataclass
class Conditions:
    """Class for keeping track of an item in inventory.

    Example:
    >>> current_conditions = Conditions(trials=100)
    >>> current_conditions.trials
    100
    """

    def _create_participant_id(self, length: int = 8):
        """Create a random participant id"""
        participant_id = "".join(
            random.choice(string.ascii_uppercase + string.digits)
            for i in range(length)
        )
        return participant_id

    name: str
    version: str
    n_repeats: int
    break_each_n_repeats: int
    method: str
    parameters: dict
    participant: str = _create_participant_id(8)

    def get_trial_handler(self) -> data.TrialHandler:
        """Create a trial handler from the conditions file

        Info:
            https://psychopy.org/api/data.html#psychopy.data.TrialHandler
        """
        # Get the keys and values from the parameters dictionary
        keys = list(self.parameters.keys())
        values = list(self.parameters.values())

        # Generate all combinations
        combinations = list(product(*values))

        # Create dictionaries from combinations as trial_list
        trial_list = [
            dict(zip(keys, combination)) for combination in combinations
        ]

        logging.info("Trial list (conditions): trial_list")

        trial_handler = data.TrialHandler(
            trialList=trial_list,
            nReps=self.n_repeats,
            method=self.method,
            name="Experiment",
        )

        return trial_handler


def import_conditions(
    file_name: str = "conditions.yml",
) -> Conditions:
    """Import conditions from yml file and store it as a dataclass."""

    with open(file_name, encoding="utf-8") as file:
        yml = yaml.safe_load(file.read())
        conditions = Conditions(**yml)

    return conditions


if __name__ == "__main__":
    import doctest

    doctest.testmod()
