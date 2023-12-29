import time
from Logger import Logger


def factorial(x: int) -> int:
    # starting a timer inside a recursive function
    Logger.start_timer(category="Others", recursive_counted=True)

    if x > 1:
        x = x * factorial(x - 1)
    time.sleep(.1)

    # stopping a timer inside a recursive function
    Logger.stop_timer(category="Others")
    return x


# specify which categories to log or time
Logger.logged_categories = ["Processing", "Others"]

i: int = 20

# starting the main timer
Logger.start_timer(msg="Starting main timer")

time.sleep(1)

# starting the second main timer, with key to differentiate timers
Logger.start_timer(key="Second Main Timer", msg="Starting Second Main Timer")
# logging before factorial call
Logger.log("Processing", f"calling factorial for {i}:")

print(f"{i} Factorial is {factorial(i)}")

# stopping the second main timer (order between different timers does not matter)
Logger.stop_timer(key="Second Main Timer", msg="Stopping Second Main Timer")
# stopping the main timer (order between different timers does not matter)
Logger.stop_timer(msg="Stopping main timer")
# printing all logged or timed categories
print(f"All logged categories {Logger.all_categories}")
