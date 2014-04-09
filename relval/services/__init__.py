__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

from apscheduler.scheduler import Scheduler
from relval.services.concurrent_executor import get_and_start_concurrent_executor, LogCleanUpTask

tasks_executor = get_and_start_concurrent_executor()

# Scheduler configuration
scheduler = Scheduler()
scheduler.start()

########################################################
# Jobs that should be executed after particular interval
########################################################

@scheduler.interval_schedule(seconds=10)
def clean_up_job():
    tasks_executor.add_task(LogCleanUpTask())



