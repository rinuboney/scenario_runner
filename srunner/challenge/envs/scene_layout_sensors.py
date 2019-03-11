
import time

import util.scene_layout as scene_layout_parser
from srunner.challenge.envs.sensor_interface import threaded

class SceneLayoutMeasurement(object):
    def __init__(self, data, frame_number):
        self.data = data
        self.frame_number = frame_number

class SceneLayout(object):
    def __init__(self, world):
        """

        :param acc:
        :param reading_frequency:
        """

        # The static scene dictionary of all the entire scene layout.
        self.static_scene_dict = scene_layout_parser.get_scene_layout(world)
        # Callback attribute to set the function being used.
        self._callback = None

        # Just connect the scene layout directly with the sensors
        self.read_scene_layout()

    def __call__(self):
        return self.static_scene_dict

    def read_scene_layout(self):
        if self._callback is not None:
            self._callback(SceneLayoutMeasurement(self.__call__(), 0))

    def listen(self, callback):
        # Tell that this function receives what the producer does.
        self._callback = callback

class ObjectMeasurements(object):
    def __init__(self, data, frame_number):
        self.data = data
        self.frame_number = frame_number


class ObjectFinder(object):
    """
    Pseudo sensor that gives you the position of all the other dynamic objects and their states
    """

    def __init__(self,  world, reading_frequency):
        """
            The object finder is used to give you the positions of all the
            other dynamic objects in the scene and their properties.
        """
        # Give the entire access there

        # The vehicle where the class reads the speed
        self._world = world
        # How often do you look at your speedometer in hz
        self._reading_frequency = reading_frequency
        self._callback = None
        #  Counts the frames
        self._frame_number = 0
        self._run_ps = True
        self.find_objects()

    def __call__(self):
        """ We here work into getting all the dynamic objects """
        return scene_layout_parser.get_dynamic_objects

    @threaded
    def find_objects(self):

        latest_speed_read = time.time()
        while self._run_ps:
            if self._callback is not None:
                capture = time.time()
                if capture - latest_speed_read > (1 / self._reading_frequency):
                    self._callback(ObjectMeasurements(self.__call__(), self._frame_number))
                    self._frame_number += 1
                    latest_speed_read = time.time()
                else:
                    time.sleep(0.001)

    def listen(self, callback):
        # Tell that this function receives what the producer does.
        self._callback = callback

    def destroy(self):
        self._run_ps = False

