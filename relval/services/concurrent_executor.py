__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

from concurrent import futures
from Queue import Queue
from threading import Thread
from relval import app
from relval.services.commands_service import CommandsService


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
        self.workers = workers
        self.stopped = False
        self.tasks_queue = Queue()

    def add_task(self, task):
        if not isinstance(task, AbstractTask):
            raise Exception("Task should be subclass of AbstractTask")
        self.tasks_queue.put(task)

    def stop(self):
        self.stopped = True

    def run(self):
        with futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            while not self.stopped:
                task = self.tasks_queue.get()
                app.logger.info("Added task {0} for concurrent execution".format(self.name))
                executor.submit(task.run)

            executor.shutdown()


class SubmitForTestingTask(AbstractTask):
    def __init__(self, request_id):
        AbstractTask.__init__(self, "Submit for testing request_id={0}".format(request_id))
        self.request_id = request_id
        self.commands_service = CommandsService()

    def run(self):
        try:
            self.result = self.commands_service.submit_for_testing(self.request_id)
        except Exception as ex:
            self.exception = ex