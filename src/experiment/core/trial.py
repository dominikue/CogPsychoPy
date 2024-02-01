from psychopy import data, core, event, visual, logging

from experiment.utils.config import Config


def run_trial(
    win: visual.Window,
    config: Config,
    trial_handler: data.TrialHandler,
) -> None:
    """Run a trial:
        - (1) run the task
        - (2) save the results of the task

    Args:
        win: (psychopy) visual.Window
        config: (Config) Dataclass with the configuration of the experiment
        trial_handler: (data.TrialHandler) The current active TrialHandler

    Notes:
        Important attributes of the trialhandler:

        .data - a dictionary (or more strictly, a `DataHandler` sub-
            class of a dictionary) of numpy arrays, one for each data
            type stored
        .trialList - the original list of dicts, specifying the conditions
        .thisIndex - the index of the current trial in the original
            conditions list
        .nTotal - the total number of trials that will be run
        .nRemaining - the total number of trials remaining
        .thisN - total trials completed so far
        .thisRepN - which repeat you are currently on
        .thisTrialN - which trial number *within* that repeat
        .thisTrial - a dictionary giving the parameters of the current
            trial
        .finished - True/False for have we finished yet
        .extraInfo - the dictionary of extra info as given at beginning
    """

    clock_task = core.Clock()

    # ----------------------------------------------------------------------------------
    # (1) Run task
    key_pressed = run_task(
        win,
        config,
        trial_handler.thisTrial,
    )

    # ----------------------------------------------------------------------------------
    # (2) Save the trial to the csv file
    # example: thisExp.addData('additionalData', 'test')

    exp = trial_handler.getExp()

    exp.addData("datestr", data.getDateStr())
    exp.addData("key_pressed", key_pressed)
    exp.addData("time_start_trial", clock_task.getTime())

    logging.exp("Trial: Finished. \n")
    logging.flush()  # displaying the log for the trial in the console


def run_task(
    win: visual.Window,
    config: Config,
    conditions: dict,
):
    """
    Run a task.
    """
    logging.info("Start the task")
    event.clearEvents()  # clear the event buffer to start with

    if config.debug:
        print("Run task in debug mode")

    stim_test = visual.TextStim(
        win,
        text=f"{conditions}\n-- press key --",
        wrapWidth=1200,
        autoLog=True,
    )
    stim_test.draw()
    win.flip()

    pressed_key = event.waitKeys()

    return pressed_key
