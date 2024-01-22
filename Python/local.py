import os
import sys
import multiprocessing
from typing import Dict, Optional, List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, DirModifiedEvent
import logging
import pyperclip

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class event_handler(FileSystemEventHandler):
    def __init__(self, handler) -> None:
        self.handler: ProcessHandler = handler
        self.detached_handler: Optional[None | multiprocessing.Process] = None
        super().__init__()

    def on_modified(self, event: Optional[FileModifiedEvent | DirModifiedEvent]):
        # detach event handler
        if event.src_path not in self.handler.monitor:
            return

        if self.detached_handler:
            if self.detached_handler.is_alive():
                logging.debug("Terminating existing wrapper")
                self.detached_handler.terminate()

        logging.info("Changed: %s", event.src_path)
        self.detached_handler = multiprocessing.Process(
            target=ProcessHandler.on_modified_handler, args=[self.handler, event]
        )

        logging.debug("Starting new wrapper")
        self.detached_handler.start()


class ProcessHandler:
    def __init__(
        self,
        main,
        props: Dict[str, str],
        monitor: List[str],
        timeout: float = -1,
    ) -> None:
        self.main: function = main
        self.props: Dict[str, str] = props
        self.timeout: float = timeout

        self.logger: logging.Logger = logging.getLogger("AutoReload")
        self.logger.setLevel(logging.DEBUG)

        # Resolve files to monitor
        self.monitor :List[str] = [os.path.abspath(p) for p in monitor]

        # Get a common parent directory
        parent_dir: str = os.path.commonpath(self.monitor)
        if not os.path.isdir(parent_dir):
            parent_dir: str = os.path.dirname(parent_dir)

        # Process
        self.process: Optional[None | multiprocessing.Process] = None

        # Schedule observer
        logging.info("Monitoring on parent=%s monitor=%s", parent_dir, monitor)

        observer = Observer()
        eh :event_handler = event_handler(handler=self)
        observer.schedule(eh, parent_dir)
        observer.start()

        # Fix: Ctrl+C to terminate
        # Do not join observer, stop it here
        try:
            sys.stdin.read()
        except KeyboardInterrupt:
            # Terminate all other processes
            if eh.detached_handler and eh.detached_handler.is_alive():
                logging.info("Terminating event handler")
                eh.detached_handler.terminate()
            
            if self.process and self.process.is_alive():
                logging.info("Terminating main process")
                self.stop_process()
            observer.stop()

    def on_modified_handler(self, event):
        self.stop_process()
        self.logger.info("Changed: %s", event.src_path)
        self.start_process()

    @staticmethod
    def local_main(props, main_fn):
        logging.debug("Calling actual function")
        sys.stdin = open(props["input"])
        main_fn()

    def stop_process(self):
        logging.debug("Force stopping main process")
        if self.process:
            if self.process.is_alive():
                self.process.terminate()
            self.process = None

    def start_process(self):
        logging.debug("Starting main process")
        self.copy_code()
        self.stop_process()

        self.process = multiprocessing.Process(
            target=ProcessHandler.local_main, args=[self.props, self.main]
        )

        logging.debug("joining timeout = %d", self.timeout)
        self.process.start()

        if self.timeout > 0:
            self.process.join(self.timeout)
            if self.process:
                if self.process.is_alive():
                    try:
                        logging.info("Terminating process (timeout=%.2fs)", self.timeout)
                        self.process.terminate()
                    except Exception as err:  # type: ignore
                        logging.error(err)

    def copy_code(self):
        with open(self.props["code"]) as fd:
            pyperclip.copy(fd.read())
