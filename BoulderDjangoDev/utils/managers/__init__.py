"""This module provides resources for background processes. Currently, this
includes:
    (1) Image Uploading service
    (2) URL Shortening Service
"""
from config import IMAGE_QUEUE, IMAGE_SIZE, MEETUP_API_KEY
from multiprocessing import Process, Queue
from queue import Empty

from .image import UserImageManager
from .meetup import MeetupManager

import os

__all__ = ['initialize_processes', 'push_image']

def initialize_user_image_manager(queue):
    """Generates the ImageManager class and starts it."""
    ## Allows process to access the ORM
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", 
        "BoulderDjangoDev.settings"
    )
    
    from users.models import DjangoDev
    
    manager = UserImageManager(queue, DjangoDev)
    manager.run()

def initialize_meetup_manager(api_key):
    """Generates a MeetupManager class and starts it"""
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", 
        "BoulderDjangoDev.settings"
    )
    manager = MeetupManager(MEETUP_API_KEY)
    manager.run()

def initialize_processes():
    """Initializes all background processes."""

    print("Initializing background processes...")
    Process(
        target=initialize_user_image_manager,
        args=(IMAGE_QUEUE,)).start()
    Process(
        target=initialize_meetup_manager,
        args=(MEETUP_API_KEY,)).start()

def push_image(pk, image_data):
    """Pushes an image onto the image queue"""
    message = {"pk": pk, "data": image_data}
    IMAGE_QUEUE.put(message)
