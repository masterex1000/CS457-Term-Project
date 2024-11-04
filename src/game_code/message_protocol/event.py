"""
This class is an abstract base class that can be used to implement shared functionality
 for the various different message types used in the game
"""
from abc import ABC, abstractmethod


class Event(ABC):
    """ The event class represents an interface specifying the event type and some on_event logic for subclasses """
    @property
    @abstractmethod
    def action(self):
        """ The action property specifies the type of event """
        return NotImplemented

    @abstractmethod
    def to_dict(self):
        """
        Useful method to have, especially since we're using json format for messages
         Python dicts are effectively json syntax
        """
        return NotImplemented
