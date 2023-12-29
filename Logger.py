import sys
import datetime


class Logger:
    """
    A simple, powerful, flexible and very easy to use logging and timer class.
    You can log by categories and create many timers without any parameters and can be set inside a recursive function
    without affecting the main result.

    You can choose which categories to be logged or timed. While logging needs category, timer operations make
    categories optional. But without a category every time you run your code, it will be timed.

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
    """
    logged_categories: list[str] = []  # must be modified at runtime by the user to allow logging and timer functions
    all_categories: list[str] = []  # readonly tho the user as it accumulates all requested categories
    output = sys.stdout  # stdout by default, but can be modified by the user at any time to change the output
    print_timestamp: bool = True  # if True, it will print timestamp with each log and timer output.
    full_timer_format: bool = False  # if true hours minutes etc. will be printed even if zeros
    timestamp_format: str = "%Y-%m-%d %H:%M:%S"  # format for all timestamps in logging and timer

    # private internal usage variables
    _timer_stack: list[str] = []  # internal usage, not to be modified by the user (keys stack)
    _timer_time_stack: list[datetime] = []  # internal usage, not to be modified by the user (timestamp stack)
    _timer_pass_stack: list[str] = []  # internal usage, not to be modified by the user (keys to ignore stack)

    @staticmethod
    def log(category: str, msg: object, sep: str = ' ', end: str = "\n", flush: bool = False):
        """
        This method will log any msg or object to sys.stdout or any other output stream
        if the category is in the categories that are to be logged.

        Changes to the Logger.logged_categories list is a must for the category to be logged, since only
        categories in that list will be logged

        The all_categories list will be filled automatically with any category passed to the method or
        any other method in Logger class, so this variable is read only from the user point of view

        sep, end and flush args will be passed to the print statement as is with no modification

            :param category: category to be logged, if not in the all_categories it will be added to all_categories
            :param msg: the object that will be logged or printed in the output stream
            :param sep: the seperator that will be passed to print statement
            :param end: end arg will be passed to the print statement end arg as is with no modification
            :param flush: flush will be passed to the print statement flush arg as is with no modification

        """
        dt: datetime.datetime = datetime.datetime.now()
        if category not in Logger.all_categories:
            Logger.all_categories.append(category)
        if category in Logger.logged_categories:
            print(dt.strftime(Logger.timestamp_format) if Logger.print_timestamp else "", msg
                  , sep=sep, end=end, flush=flush, file=Logger.output)

    @staticmethod
    def start_timer(category: str = "", key: str = "", msg: object = "Starting Timer "
                    , recursive_counted: bool = False, end: str = "\n", sep: str = ' ', flush: bool = False):
        """
        This method will start the timer and record the timestamp.
        A msg will be printed to sys.stdout or any other output stream if the category is in the categories
        that are to be logged or if no category is supplied.

        to handle recursive function automatically, recursive_counted should be set to False (in start_timer) and
        the start_timer and stop_timer methods should be both called at the beginning and before end or return of the
        function that calls itself recursively.

        Changes to the Logger.logged_categories list is a must for the category to be timed.
        however, if no category is supplied, the timer will start or stop nonetheless.

        The all_categories list will be filled automatically with any category passed to the method or
        any other method in Logger class, so this variable is read only from the user point of view

        sep, end and flush args will be passed to the print statement as is with no modification

            :param category: Category to be logged, if not in the logged_categories it will be added to all_categories
            :param msg: The object that will be logged or printed in the output stream
            :param key: Since many timers can start or stop at any given moment, key is set to distinguish each timer.
                        if no key is supplied, the calling function will be used as key,
                        start_timer and stop_timer must be paired with the same key to work properly
            :param recursive_counted: If True, all recursive calls will be timed separately
            :param sep: The seperator that will be passed to print statement
            :param end: end arg will be passed to the print statement end arg as is with no modification
            :param flush: flush arg will be passed to the print statement flush arg as is with no modification

        """
        dt: datetime.datetime = datetime.datetime.now()
        empty_key: bool = False
        if category != "" and category not in Logger.all_categories:
            Logger.all_categories.append(category)
        if category == "" or category in Logger.logged_categories:
            if key == "":
                key = sys._getframe(1).f_code  # Key will be assigned to Caller function name (inspect was slower)
                empty_key = True
            if len(Logger._timer_stack) == 0 or key not in Logger._timer_stack or recursive_counted:
                Logger._timer_stack.append(key)
                Logger._timer_time_stack.append(dt)
                print(dt.strftime(Logger.timestamp_format) if Logger.print_timestamp else "", msg
                      , key if not empty_key else str(key).partition(",")[0].partition("code object")[2]
                      , sep=sep, end=end, flush=flush, file=Logger.output)
            else:
                Logger._timer_pass_stack.append(key)

    @staticmethod
    def stop_timer(category: str = "", key: str = "", msg: object = "Stop Timer "
                   , sep: str = ' ', end: str = "\n", flush: bool = False):
        """
        This method will stop the timer and record the time period since the timer with the same key has started.
        A msg will be printed to sys.stdout or any other output stream if the category is in the categories
        that are to be logged or if no category is supplied.

        to handle recursive function automatically, recursive_counted should be set to False (in start_timer) and
        the start_timer and stop_timer methods should be both called at the beginning and before end or return of the
        function that calls itself recursively.

        Changes to the Logger.logged_categories list is a must for the category to be timed.
        however, if no category is supplied, the timer will start or stop nonetheless.

        The all_categories list will be filled automatically with any category passed to the method or
        any other method in Logger class, so this variable is read only from the user point of view

        sep, end and flush args will be passed to the print statement as is with no modification

            :param category: Category to be logged, if not in the logged_categories it will be added to all_categories
            :param key: Since many timers can start or stop at any given moment, key is set to distinguish each timer.
                        if no key is supplied, the calling function will be used as key,
                        start_timer and stop_timer must be paired with the same key to work properly
            :param msg: The object that will be logged or printed in the output stream
            :param sep: The seperator that will be passed to print statement
            :param end: end arg will be passed to the print statement end arg as is with no modification
            :param flush: flush arg will be passed to the print statement flush arg as is with no modification

        """
        dt: datetime = datetime.datetime.now()
        empty_key: bool = False
        if category != "" and category not in Logger.all_categories:
            Logger.all_categories.append(category)
        if category == "" or category in Logger.logged_categories:
            if key == "":
                key = sys._getframe(1).f_code  # Key will be assigned to Caller function name (inspect was slower)
                empty_key = True
            if len(Logger._timer_pass_stack) > 0 and key in Logger._timer_pass_stack:
                i: int = Logger._timer_pass_stack.index(key, -1)
                Logger._timer_pass_stack.pop(i)
                return
            if key in Logger._timer_stack:
                i: int = Logger._timer_stack.index(key, -1)
                Logger._timer_stack.pop(i)
                st: datetime = Logger._timer_time_stack.pop(i)
                ti = dt - st
                print(dt.strftime(Logger.timestamp_format) if Logger.print_timestamp else "", msg
                      , Logger.format_timedelta_in_hours_etc(ti, full_format=Logger.full_timer_format)
                      , key if not empty_key else str(key).partition(",")[0].partition("code object")[2]
                      , sep=sep, end=end, flush=flush, file=Logger.output)

    @staticmethod
    def format_timedelta_in_hours_etc(td: datetime.timedelta, full_format: bool = False) -> str:
        """
        Returns a formatted timedelta object in the format 00h:00m:00s:000ms:000μs:000ns (hours can exceed 24)
        :param td: a timedelta object to be formatted
        :param full_format: whether zeroed values will be returned or not like 00h:00m:00s
        :return: the string containing the formatted timedelta object in the following
                 format 00h:00m:00s:000ms:000μs:000ns (hours can exceed 24 and go infinite)
        """
        hours, remainder = divmod(td.total_seconds(), 3600)
        minutes, remainder = divmod(remainder, 60)
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(remainder)
        remainder -= seconds
        ml_seconds, remainder = divmod(remainder * 1000, 1)
        mc_seconds, remainder = divmod(remainder * 1000, 1)
        ns_seconds, remainder = divmod(remainder * 1000, 1)
        ml_seconds = int(ml_seconds)
        mc_seconds = int(mc_seconds)
        ns_seconds = int(ns_seconds)
        s: str = f"{hours:02d}h:{minutes:02d}m:{seconds:02d}s:{ml_seconds:03d}ms:{mc_seconds:03d}μs:{ns_seconds:03d}ns"
        if not full_format:
            if not hours:
                s = s.removeprefix("00h:")
            if not minutes:
                s = s.removeprefix("00m:")
            if not seconds:
                s = s.removeprefix("00s:")
            if not ml_seconds:
                s = s.removeprefix("000ms:")
            if not mc_seconds:
                s = s.removeprefix("000μs:")
        return s
