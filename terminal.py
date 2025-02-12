from contextlib import contextmanager
import time
import threading


class Log:
    DO_LOG: bool = True # WARNING: This is a class variable and will affect all instances of Log globally

    @staticmethod
    def error(message: str) -> None:
        if not Log.DO_LOG:
            return
        print("\033[1m[\033[91mFAIL\033[0m]\033[0m", message)
    
    @staticmethod
    def warn(message: str) -> None:
        if not Log.DO_LOG:
            return
        print("\033[1m[\033[93mWARN\033[0m]\033[0m", message)

    @staticmethod
    def okay(message: str) -> None:
        if not Log.DO_LOG:
            return
        print("\033[1m[\033[92mOKAY\033[0m]\033[0m", message)
    
    @staticmethod
    def info(message: str) -> None:
        if not Log.DO_LOG:
            return
        print("\033[1m[\033[94mINFO\033[0m]\033[0m", message)

class Item:
    @staticmethod
    def checked(message: str, indent: bool = True) -> None:
        if indent:
            print("  ", end="")
        print("\033[92m✔\033[0m", message)

    @staticmethod
    def failed(message: str, indent: bool = True) -> None:
        if indent:
            print("  ", end="")
        print("\033[91m✘\033[0m", message)

    @staticmethod
    def skipped(message: str, indent: bool = True) -> None:
        if indent:
            print("  ", end="")
        print("\033[93m⚠\033[0m", message)

    @staticmethod
    def info(message: str, indent: bool = True) -> None:
        if indent:
            print("  ", end="")
        print("\033[94m→\033[0m", message)

class Cursor:
    @staticmethod
    def hide() -> None:
        print("\033[?25l", end="", flush=True)

    @staticmethod
    def show() -> None:
        print("\033[?25h", end="", flush=True)

def clear() -> None:
    print("\033[H\033[J", end="", flush=True)

def await_press_enter() -> None:
    if input("Press Enter to continue...") != "":
        exit(0)

@contextmanager
def spinner(message: str = "Loading", complete_message: str = None):
    if complete_message is None:
        complete_message = message


    resulted_in_error = False
    Cursor.hide()
    stop_spinner = threading.Event()

    def spin():
        frames: list[str] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        while not stop_spinner.is_set():
            for frame in frames:
                if stop_spinner.is_set():
                    break
                print(f"\r{frame} {message.removesuffix('...')}...", end="", flush=True)
                time.sleep(0.1)

    spinner_thread = threading.Thread(target=spin)
    spinner_thread.start()
    try:
        yield
    except:
        resulted_in_error = True
    finally:
        stop_spinner.set()
        spinner_thread.join()
        print("\r\033[K", end="", flush=True)
        Cursor.show()
        if resulted_in_error:
            Item.failed(f"[FAILED] {message}", indent=False)
        else:
            Item.checked(complete_message, indent=False)
