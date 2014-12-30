import threading
import Queue

class Consumer(threading.Thread):

    def __init__(self, id, work_queue, result_queue, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self.id = id
        self.setDaemon(True)
        self._work_queue = work_queue
        self._result_queue = result_queue

        self.start()

    def run(self):
        while True:
            callable, args, kargs = self._work_queue.get()

            if callable is None:
                # Manager quits
                break

            res = callable(*args, **kargs)
            self._work_queue.task_done()
            self._result_queue.put(res)

class ThreadPool(object):
    def __init__(self, max_worker=10):
        self.work_queue = Queue.Queue()
        self.result_queue = Queue.Queue()
        self.consumers = []

        # Recuruit consumers
        for i in range(max_worker):
            consumer = Consumer(i, self.work_queue, self.result_queue)
            self.consumers.append(consumer)

    '''
    We require this class always runs on main thread, so we don't consider
    synchronization of this class
    '''
    def wait_for_complete(self):
        self.work_queue.join()
        res_arr = []
        while not self.result_queue.empty():
            res_arr.append(self.result_queue.get())
            self.result_queue.task_done()
        return res_arr

    def destroy(self):
        while len(self.consumers):
            self.work_queue.put((None, [], {}))
            consumer = self.consumers.pop()
            consumer.join()
            if consumer.isAlive() and not self.work_queue.empty():
                self.consumers.append(consumer)

    def add_job(self, job, *args, **kwargs):
        self.work_queue.put((job, args, kwargs))
