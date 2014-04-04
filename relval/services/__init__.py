__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

from relval.services.concurrent_executor import get_and_start_concurrent_executor

tasks_executor = get_and_start_concurrent_executor()
