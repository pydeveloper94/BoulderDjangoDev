from binascii import a2b_base64
from config import IMAGE_QUEUE, IMAGE_SIZE, MEETUP_API_KEY
from mimetypes import guess_extension, guess_type
from multiprocessing import Process, Queue
from PIL import Image
from queue import Empty

from users.models import DjangoDev

import os
import requests
import sys
import time

class UserImageManager(object):
    """Class which manages all image uploads.
    This class will accept the dictionaries of the following type
    {
        "pk": int,
        "data": string,     # This should be the location
    }
    """
    queue = None
    
    def __init__(self, image_queue, model):
        self.queue = image_queue
        self.model = model

    def run(self):
        """Main run method. Checks the queue for a new message every second."""
        while True:
            try:
                message = self.queue.get(block=False)
                self.handle_message(message)
            except Empty:
                time.sleep(1)
    
    def handle_message(self, message):
        """Main method for handling an image upload."""
        data = message.get('data')
        pk = message.get('pk')
        if (data == None) or (pk == None):
            return
        try:
            ## Load data into a file object
            extension = guess_extension(guess_type(data)[0])
            binary_data = a2b_base64(data.split(',')[1])
            name = self.generate_name(extension)
            with open(name, 'wb') as image:
                image.write(binary_data)
            ## Formage image
            self.format_image(name)
            ## Upload the image onto the server and save the user
            url = self.upload_image(name)
            print(url)
            self.update_user(pk, url)
            ## Delete image
            os.remove(name)
        except Exception as e:
            print("Error in the UserImageManager", e)
    
    def generate_name(self, extension=None):
        """Generates an image file name."""
        if type(extension) != type(''):
            raise Exception("You did not pass a valid string extension, such "
                "as .jpg or .png into generate_name()")
        return "./tmp/%f%s" % (time.time(), str(extension))

    def format_image(self, name):
        """Formats the image into a thumbnail"""
        image = Image.open(name)
        image.thumbnail(IMAGE_SIZE)
        image.save(name)

    def upload_image(self, name):
        """Takes a file handler, creates a file object, and returns a url"""
        with open(name, 'rb') as image:
            files = {'file': image}
            req = requests.post('http://uploads.im/api', files=files)
        data = req.json()
        if data.get('status_code') == 200:
            return data['data']['img_url']
        else:
            ## Log the request
            return None

    def update_user(self, pk, url):
        """Updates a users image url."""
        user = self.model.objects.get(pk=pk)
        user.image = url
        user.save()
