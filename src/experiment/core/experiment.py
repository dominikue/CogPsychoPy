import yaml

from psychopy import data, core, logging, event, visual

from experiment.core.trial import run_trial
from experiment.utils.conditions import Conditions
from experiment.utils.config import Config


def run_experiment(
    config: Config,
    conditions: Conditions,
) -> None:
    """Run the experiment.

    Args:
        TODO add args
    Returns:
        None (psychopy window, data file (.csv, .log, .psydata))
    """

    # Open a PsychoPy window, show the image, collect a keypress, close.
    win = visual.Window(
        (1200, 500),  # only for debug in non fullscreen mode
        screen=config.screen.id,
        units="pix",
        fullscr=config.fullscreen,
    )

    logging.info("Win size: " + str(win.size))

    win.setMouseVisible(False)

    event.globalKeys.add(
        key="q", modifiers=["ctrl"], func=core.quit, name="shutdown"
    )

    # ----------------------------------------------------------------------------------
    # EXPERIMENT HANDLER

    this_exp = data.ExperimentHandler(
        name=conditions.name,
        version=conditions.version,
        extraInfo={"participant": conditions.participant},
        dataFileName=config.filepath_participant,  # using our string with data/name_date
        autoLog=True,
    )

    # add a trial handler to the experiment handler
    this_exp.addLoop(conditions.get_trial_handler())

    logging.log(level=logging.DEBUG, msg="started experiment")
    logging.flush()

    # ----------------------------------------------------------------------------------
    # LOOPING: Loops through each loop and each trial
    for current_trialhandler in this_exp.loops:
        print("Startet loop: ", current_trialhandler.thisTrial)

        # Show instructions and current trial loop name
        instruction1 = config.text.instruction
        instruction2 = config.text.instruction_start

        text_instruction_loop = f"{instruction1}\n\n\
            loop name: {current_trialhandler.name}\n\n\
            participant: '{conditions.participant}'\n\n\
            {50*'-'}\n\n\
            {instruction2}"  # TODO change string

        instruction_stim = visual.TextStim(
            win, text=text_instruction_loop, wrapWidth=1200, autoLog=False
        )

        instruction_stim.draw()
        win.flip()

        event.waitKeys()

        logging.flush()
        print(f"\n\n\n{100*'*'}")  # clear the console

        # ----------------------------------------------------------------------------------
        # TRIALS
        # Loop through the trials
        for _ in current_trialhandler:
            run_trial(win, config, current_trialhandler)

            # Important for csv file writing: Call after adding the response.
            this_exp.nextEntry()

        logging.info("finished trial loop")

        win.flip()
        text_end = visual.TextStim(
            win, text="End of the experiment.", wrapWidth=1200, autoLog=False
        )
        text_end.draw()

        for _ in range(20):
            win.flip()

        logging.flush()

    win.close()

    # ----------------------------------------------------------------------------------
    # EXPORT DATA
    # (1) Automatically export for files https://www.psychopy.org/general/dataOutputs.html

    # (2) Export of the conditions file
    with open(
        config.filepath_participant + "_conditions.yaml", "w", encoding="utf-8"
    ) as outfile:
        yaml.dump(conditions, outfile, default_flow_style=False)

    # (3) Export of the config file
    with open(
        config.filepath_participant + "_config.yaml", "w", encoding="utf-8"
    ) as outfile:
        yaml.dump(config, outfile, default_flow_style=False)

    logging.flush()
    core.quit()


def __instruction_loop():
    # TODO add instruction loop
    pass
