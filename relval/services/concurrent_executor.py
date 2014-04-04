from relval.services.commands_service import CommandsService

__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

from concurrent import futures
from Queue import Queue, Empty
from threading import Thread
from relval import app


__executor_instance = None


def get_and_start_concurrent_executor(*args, **kwargs):
    """ Creates singleton ConcurrentExecutor instance and starts immediatly
    """
    global __executor_instance
    if not __executor_instance or __executor_instance.is_stopped():
        __executor_instance = ConcurrentExecutor(*args, **kwargs)
        __executor_instance.start()
    print "Instance", __executor_instance
    return __executor_instance


class AbstractTask(object):
    def __init__(self, name):
        self.name = name
        self.result = None
        self.exception = None

    def run(self):
        raise NotImplementedError("You should extend AbstractTask and override run method")


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
                    task = self.tasks_queue.get(True, 5)
                    app.logger.info("Added task '{0}' for concurrent execution".format(task.name))
                    executor.submit(task.run)
                except Empty:
                    # No new tasks within 5 seconds (tasks queue is empty).
                    # Check if executor not stopped and continue work
                    pass
            app.logger.info("ConcurrentExecutor shuts down.")
            executor.shutdown()
            app.logger.info("Concurrent executor exited")


class SubmitForTestingTask(AbstractTask):
    def __init__(self, request_id):
        AbstractTask.__init__(self, "Submit for testing request_id={0}".format(request_id))
        self.request_id = request_id
        self.commands_service = CommandsService()

    def run(self):
        app.logger.info("Executing task {0}".format(self.name))
        try:
            self.result = self.commands_service.submit_for_testing(self.request_id)
        except Exception as ex:
            app.logger.error("Error occurred when executing task {0}.\nWith exception: {1}".format(
                self.name, str(ex)
            ))
            self.exception = ex