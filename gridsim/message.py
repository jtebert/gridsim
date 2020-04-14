# from __future__ import annotations  # For the type checking circular import

from typing import Dict, Any, Optional, Type  # , TYPE_CHECKING

from .robot import Robot

# if TYPE_CHECKING:
#     from .robot import Robot


class Message:
    def __init__(self, tx_id: Optional[int] = None,
                 content: Optional[Dict[str, Any]] = None,
                 rx_type: Type[Robot] = Robot,  # Default is any robot
                 ):
        """
        A message sent by robots. Can be either a null (empty) message if not
        arguments are provided to the constructor. Or it contains the sender's
        ID, a dictionary of content, and (optionally) the type of robot that
        receives the message.

        Parameters
        ----------
        tx_id : Optional[int], optional
            ID of the sending (transmitting) robot, by default None
        content : Optional[Dict[str, Any]], optional
            Dictionary of message keys and values, by default None. Keys must be
            strings, but values can be of any type (incumbent on receiver for
            interpretation)
        rx_type : Type[Robot], optional
            Type of the receiving robot, by default Robot (i.e., message will be
            processed by any Robot.)
        """
        # Validate the message contents
        if tx_id is None and content is None:
            # Null message
            self._tx_id = None
            self._rx_type = None
            self._content = None
            self.is_null = True
        else:
            # Non-null message must include correct receiver type and dictionary
            if not issubclass(rx_type, Robot):
                raise TypeError('Receiver type must be a subclass of Robot')
            if not isinstance(content, Dict) or \
                    not all(map(lambda k: isinstance(k, str), content.keys())):
                raise TypeError(
                    'Content must be a dictionary with string keys')
            else:
                self._tx_id = tx_id
                self._rx_type = rx_type
                self._content = content
                self.is_null = False

    def get(self) -> Optional[Dict[str, Any]]:
        """
        Get the contents of the message

        Returns
        -------
        Optional[Dict[str, Any]]
            Dictionary of the message contents
        """
        return self._content

    def tx_id(self) -> Optional[int]:
        """
        Get the ID (32-bit integer) of the robot that sent the message

        Returns
        -------
        Optional[int]
            ID of the sending (transmitting) robot
        """
        return self._tx_id

    def __str__(self) -> str:
        """Format the message as a human-readable string

        Returns
        -------
        str
            Friendly message format (or says it's an empty message)
        """
        if self.is_null:
            return "NULL message"
        else:
            return '{id} -> {type}: {contents}'.format(
                id=self._tx_id,
                type=self._rx_type,
                contents=self._content
            )
