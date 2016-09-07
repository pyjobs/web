# -*- coding: utf-8 -*-
from tg import config
from contextlib import contextmanager
from fasteners import InterProcessLock


def _compute_lock_name(desired_name):
    project_name = config.get('processes.project_name')
    instance_name = config.get('processes.instance_name')
    lock_name_prefix = '%s_%s' % (project_name, instance_name)
    return '%s_%s' % (lock_name_prefix, desired_name)


@contextmanager
def acquire_inter_process_lock(lock_name):
    # Lock preventing simultaneous crawling processes
    lock_name = _compute_lock_name(lock_name)
    lock = InterProcessLock('/tmp/%s' % lock_name)
    acquired_lock = lock.acquire(blocking=False)

    try:
        yield acquired_lock
    finally:
        if acquired_lock:
            lock.release()
