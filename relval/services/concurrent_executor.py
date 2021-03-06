from relval.services.log_manager import LogsManager

__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

from concurrent import futures
from Queue import Queue, Empty
from threading import Thread
from relval import app
from relval.services.commands_service import CommandsService


__executor_instance = None


def get_and_start_concurrent_executor(*args, **kwargs):
    """ Creates singleton ConcurrentExecutor instance and starts immediately
    """
    global __executor_instance
    if not __executor_instance or __executor_instance.is_stopped():
        __executor_instance = ConcurrentExecutor(*args, **kwargs)
        __executor_instance.start()
    print "Instance", __executor_instance
    return __executor_instance


class AbstractTask(object):
    """ Abstract task to. In order to create custom task extend this class and override internal_run method.
    """
    def __init__(self, name):
        self.name = name
        self.result = None
        self.exception = None

    def run(self):
        app.logger.info("Executing task {0}".format(self.name))
        try:
            self.internal_run()
        except Exception as ex:
            app.logger.error("Error occurred when executing task {0}.With exception:\n{1}".format(
                self.name, str(ex)
            ))
            self.exception = ex

    def internal_run(self):
        """ You should override this method for custom task logic.
        """
        raise NotImplementedError("You should extend AbstractTask and override internal_run method")


class ConcurrentExecutor(Thread):
    """ Concurrent executor executes tasks from queue in separate thread.
        Workers parameter specifies how many workers at the same time should process tasks
    """

    def __init__(self, workers=4):
        """ Don't use this constructor directly.
            Instead use factory function get_concurrent_executor()
        """
        Thread.__init__(self)
        self.workers = workers
        self.timeout = 5      # timeout in seconds. After this time executor check for exit signal and waits for new tasks again.
        self.stopped = False  # flag indicates that executor get signal to stop
        self.tasks_queue = Queue()

    def add_task(self, task):
        if not isinstance(task, AbstractTask):
            raise Exception("Task should be subclass of AbstractTask")
        self.tasks_queue.put(task)

    def stop(self):
        self.stopped = True
        self.join()

    def is_stopped(self):
        return self.stopped

    def run(self):
        with futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            while not self.stopped:
                try:
                    task = self.tasks_queue.get(True, self.timeout)
                    app.logger.info("Added task '{0}' for concurrent execution".format(task.name))
                    executor.submit(task.run)
                except Empty:
                    # No new tasks within 5 seconds (tasks queue is empty).
                    # Check if executor not stopped and continue work
                    app.logger.info("No new task in ConcurrentExecutor within {0} sec. Waiting for task...".format(self.timeout))
                    pass
            app.logger.info("ConcurrentExecutor shuts down.")
            executor.shutdown()
            app.logger.info("Concurrent executor exited")


class SubmitForTestingTask(AbstractTask):
    def __init__(self, request_id):
        AbstractTask.__init__(self, "Submit for testing request_id={0}".format(request_id))
        self.request_id = request_id
        self.commands_service = CommandsService()

    def internal_run(self):
        self.result = self.commands_service.submit_for_testing(self.request_id)


class LogCleanUpTask(AbstractTask):
    def __init__(self):
        AbstractTask.__init__(self, "Clean up old log files")
        self.logs_manager = LogsManager()

    def internal_run(self):
        self.logs_manager.delete_old_test_log_files()