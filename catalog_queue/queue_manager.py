import json
import redis
import uuid
from datetime import datetime
from django.conf import settings
from django.utils.module_loading import import_module

class TaskQueue:
    
    queue_prefix = 'task_queue'

    def __init__(self):
        self.redis_client = redis.StrictRedis(
            **settings.REDIS_QUEUE,
        )

    def get_queue_name(self, task, task_id):
        return f"{self.queue_prefix}_{task.__name__}_{task_id}"

    def enqueue(self, task, args=None, kwargs=None):
        task_id = str(uuid.uuid4())
        queue_name = self.get_queue_name(task, task_id)
        task_info = {
            'task_id': task_id,
            'name': task.__name__,
            'module': task.__module__,
            'args': args or [],
            'kwargs': kwargs or {},
        }
        self.redis_client.lpush("queues_names", queue_name)
        self.redis_client.lpush(queue_name, json.dumps(task_info))
        return task_id
    
    def process_tasks(self):
        while True:
            _, queue_name = self.redis_client.blpop("queues_names")
            _, task_info_str = self.redis_client.blpop(queue_name)
            task_info = json.loads(task_info_str)
            task_id = task_info['task_id']
            task_module = import_module(task_info['module'])
            task_callable = getattr(task_module, task_info['name'])
            try:
                result = task_callable(*task_info['args'], **task_info['kwargs'])
                result_info = {
                    'task_id': task_id,
                    'state': 'success',
                    'result': result,
                    'datetime': datetime.now().isoformat()
                }
            except Exception as ex:
                result_info = {
                    'task_id': task_id,
                    'state': 'error',
                    'result': str(ex),
                    'datetime': datetime.now().isoformat()
                }

            result_queue_name = f'result_{task_id}'
            self.redis_client.set(result_queue_name, json.dumps(result_info))
            print(result_info)

    def get_result(self, task_id):
        result_info_str = self.redis_client.get(f'result_{task_id}')
        if result_info_str:
            result_info = json.loads(result_info_str)
            return result_info
