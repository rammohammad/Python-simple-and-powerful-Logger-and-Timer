# Python simple and powerful Logger and Timer
 A very simple, yet very powerful and flexible Logger and Timer

    a simple, powerful, flexible and very easy to use logging and timer class.
    you can log by categories and create many timers without any parameters and can be set inside a recursive function
    without affecting the main result.

    you can choose which categories to be logged or timed. While logging needs category, timer operations makes
    categories optional. But without category every time you run your code it will be timed.

    No need to remove debugging messages or timer operations from your code, just select or deselect which categories
    to be logged or timed, and it shall not affect execution if not chosen.

    Timer Example:
        works from a recursive function as it will only account for the main call
        -- to start timing
        Logger.start_timer()
        -- to stop the timer, and it will automatically put the calling function name if no key is supplied
        Logger.stop_timer()


    Logging Example:
        -- to specify which categories to log or time
        Logger.logged_categories = ["Main Events", "Other Functionalities"]
        -- to log
        Logger.log("Main Events", "msg to be logged")

    class variables to be modified at runtime:
        logged_categories: list[str] = []
            must be modified at runtime by the user to allow logging and categorized timer functions
        all_categories: list[str] = []
            read only to the user as it accumulates all requested categories
        output = sys.stdout
            stdout by default, but can be modified by the user at any time to change the output
        print_timestamp: bool = True
            if True, it will print timestamp with each log and timer output
        full_timer_format: bool = False
            if True hours minutes etc. will be printed even if zeros
        timestamp_format: str = "%Y-%m-%d %H:%M:%S"
            format for all timestamps in logging and timer