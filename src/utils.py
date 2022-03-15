"""utils.py

    This module defines decorators for use in logging
    and profiling weak_schur code. They are:
    1. timer simply times the code using time.time
    2. logger redirects all output of the function
       to a logfile and appends any new output; it
       will not overwrite!

    They are composable; however, keep in mind the 
    correct order: 
        For any function func, 
        @logger
        @timer 
        def func(*args, **kwargs):
            ...
    is the best order. This saves all output of 
    `func`, with the logging information from `timer`
    into "log_func.txt".
"""
import time
from contextlib import redirect_stdout

def timer(func):
    """This is a decorator that helps us time each function
    that it decorates. It will time function execution using
    the python time module, with helpful logging messages
    that tell you which function is printing what.

    Args:
        func (_type_): This is the function we want to time.
            This part is not as important, since we plan to use
            timer as a decorator, not as a function.
    """
    def wrapper(*args, **kwargs):
        """
        This is the wrapper function that our decorator will return.
        This will itself return the results of the original function.

        Returns:
            results: the return values of `func`
        """
        PREFIX = f"TIM {func.__name__}"

        # Some prints first ...
        print("-"*30)
        print(f"{PREFIX}: Starting execution ... ")

        # This is the core
        start = time.time()
        results = func(*args, **kwargs)
        end = time.time()

        # Then we indicate that execution
        # has terminated ...
        print(f"{PREFIX}: Execution terminated ...")
        print(f"{PREFIX}: Time taken - {end-start}")
        print("-"*30)

        # And return the results of
        # the original funciton
        return results

    # This is to help composability with logger 
    wrapper.__name__ = func.__name__

    return wrapper

def logger(func):
    """This is a decorator that helps us log the output of 
    the target function. It will temporarily redirect all 
    output from sys.stdout to a logfile, with helpful logging messages
    that tell you which function is printing what, and 
    execute the function in that window. This ensures that 
    all prints and 

    Args:
        func (_type_): This is the function we want to time.
            This part is not as important, since we plan to use
            timer as a decorator, not as a function.
    """
    def wrapper(*args, **kwargs):
        """
        This is the wrapper function that our decorator will return.
        This will itself return the results of the original function.

        Returns:
            results: the return values of `func`
        """

        FILENAME = f"log_{func.__name__}.txt"
        PREFIX = f"LOG {func.__name__}"

        # Here's the core loop.
        # First we open the logfile,
        with open(FILENAME, 'a') as f:
            # Indicate that we're going to pass all
            # output to the logfile after this ...
            print(f"{PREFIX}: Redirecting output to {FILENAME} ...")
            
            # This is the core logic 
            f.write("-"*30 + "\n")
            with redirect_stdout(f):
                # Add some helpful logging before
                print(f"{PREFIX}: {time.ctime()}")

                # actually executing the function
                result = func(*args, **kwargs)

            # Now, we get our output back, so print 
            # is back to normal. Now, we save 
            # the results.
            f.write(f"RESULTS:\n{result}\n")

            # and that execution is over            
            print(f"{PREFIX}: End of execution ...")

        # return the result of the original function
        return result

    return wrapper

if __name__ == "__main__": 
    # Example use-case
    @logger
    @timer
    def add(n,m):
        """ test function for our decorators."""
        print(f"ADD adding {n} and {m}")
        return n + m


    result = add(1, 2)