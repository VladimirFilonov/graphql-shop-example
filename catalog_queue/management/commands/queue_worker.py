from django.core.management.base import BaseCommand

from catalog_queue.queue_manager import TaskQueue

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        
        queue = TaskQueue()
        queue.process_tasks()