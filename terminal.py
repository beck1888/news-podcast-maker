"""Terminal utilities for displaying progress, spinners, and status messages."""

from contextlib import contextmanager
import sys
import time
import threading
from typing import Generator


class Item:
    """Utility class for displaying status messages with colored symbols."""

    @staticmethod
    def checked(message: str, indent: bool = True) -> None:
        """Display a success message with a green checkmark.

        Args:
            message: The message to display
            indent: Whether to indent the message with two spaces
        """
        if indent:
            print("  ", end="")
        print("\033[92m✔\033[0m", message)

    @staticmethod
    def failed(message: str, indent: bool = True) -> None:
        """Display a failure message with a red X.

        Args:
            message: The message to display
            indent: Whether to indent the message with two spaces
        """
        if indent:
            print("  ", end="")
        print("\033[91m✘\033[0m", message)

    @staticmethod
    def skipped(message: str, indent: bool = True) -> None:
        """Display a warning message with a yellow warning symbol.

        Args:
            message: The message to display
            indent: Whether to indent the message with two spaces
        """
        if indent:
            print("  ", end="")
        print("\033[93m⚠\033[0m", message)

    @staticmethod
    def info(message: str, indent: bool = True) -> None:
        """Display an info message with a blue arrow.

        Args:
            message: The message to display
            indent: Whether to indent the message with two spaces
        """
        if indent:
            print("  ", end="")
        print("\033[94m→\033[0m", message)


class Cursor:
    """Utility class for controlling the terminal cursor."""

    @staticmethod
    def hide() -> None:
        """Hide the terminal cursor."""
        print("\033[?25l", end="", flush=True)

    @staticmethod
    def show() -> None:
        """Show the terminal cursor."""
        print("\033[?25h", end="", flush=True)


def clear() -> None:
    """Clear the terminal screen."""
    print("\033[H\033[J", end="", flush=True)


def await_press_enter() -> None:
    """Wait for the user to press Enter, exit if any other input is received."""
    if input("Press Enter to continue...") != "":
        sys.exit(0)


@contextmanager
def spinner(message: str = "Loading", complete_message: str = None) -> Generator[None, None, None]:
    """Display a spinner while executing a block of code.

    Args:
        message: The message to display while spinning
        complete_message: The message to display when complete (defaults to message)

    Yields:
        None

    Raises:
        KeyboardInterrupt: If the user interrupts the operation
    """
    complete_message = complete_message or message
    resulted_in_error = False
    Cursor.hide()
    stop_spinner = threading.Event()

    def spin() -> None:
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        while not stop_spinner.is_set():
            for frame in frames:
                if stop_spinner.is_set():
                    break
                print(f"\r{frame} {message.removesuffix('...')}...", end="", flush=True)
                time.sleep(0.1)

    spinner_thread = threading.Thread(target=spin)
    spinner_thread.start()
    start_time: float = time.time()
    try:
        yield
    except (KeyboardInterrupt, Exception) as e:
        resulted_in_error = True
        raise e
    finally:
        stop_spinner.set()
        spinner_thread.join()
        print("\r\033[K", end="", flush=True)
        Cursor.show()
        elapsed_time = f" ({round(time.time() - start_time, 2)} s)"
        if resulted_in_error:
            Item.failed(f"[FAILED] {message}{elapsed_time}", indent=False)
            # When dealing, print the error message
            # print(f"Error: {e}")
        else:
            Item.checked(f"{complete_message}{elapsed_time}", indent=False)


if __name__ == "__main__":
    print("This script is not meant to be run directly. Run main.py instead.")
    sys.exit(1)
