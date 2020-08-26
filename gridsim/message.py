"""
This provides a basic Message protocol for robot communication. Each message contains the ID of the
sender and a dictionary of message contents. The values of the message contents may be any type, so
the receiver must know how to process the data.

Additionally, Messages can optionally include a receiver type (``rx_type``). This is only needed if
there are multiple types of robots in the World, and you only want certain types of robots to
receive the message.

If no arguments are provided when a Message is created, it creates a null message, which signals
that the robot is not broadcasting anything.

While it is possible to extend this class, the default Message class should meet most needs.
"""

from typing import Dict, Any, Optional, Type  # , TYPE_CHECKING

from .robot import Robot


class Message:
    """A message sent by robots

    Messages can be either a null (empty) message if no arguments are provided
    to the constructor. Or it contains the sender's ID, a dictionary of content, and
    (optionally) the type of robot that receives the message.

    Parameters
    ----------
    tx_id : int, optional
        ID of the sending (transmitting) robot, by default None
    content : Dict[str, Any]], optional
        Dictionary of message keys and values, by default an empty dictionary. Keys must be
        strings, but values can be of any type (incumbent on receiver to correctly interpret
        incoming data).
    rx_type : Type[Robot], optional
        Type of the receiving robot, by default Robot (i.e., message will be processed by any
        Robot.)

    Raises
    ------
    TypeError
        If ``rx_type`` is not a subclass of :class:`~gridsim.robot.Robot`, or ``content`` is not
        a dictionary with strings for keys
    """

    def __init__(self, tx_id: Optional[int] = None,
                 content: Dict[str, Any] = {},
                 rx_type: Type[Robot] = Robot,  # Default is any robot
                 ):
        # Validate the message contents
        if tx_id is None and not content:
            # Null message
            self._tx_id = None
            self._rx_type = None
            self._content = {}
            self._is_null = True
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
                self._is_null = False

    def get(self, key: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get the contents of the message

        Parameters
        ----------
        key : str, optional
            Name of the parameter to retrieve, by default None. If not specified, a dictionary of
            all parameters will be returned.

        Returns
        -------
        Dict[str, Any] or None
            Dictionary of the message contents

        Raises
        ------
        KeyError
            If a key is provided but is not in the message contents
        """
        if key is None:
            return self._content
        else:
            return self._content[key]

    def set(self, key: str, value: Any) -> None:
        """Set the message contents

        In the message contents, set the given key to have the given value. If this is an empty
        (null) message, this will raise an error. If the key already exists, the existing value will
        be overwritten

        Parameters
        ----------
        key : str
            Key in the message contents for which to set the value
        value : Any
            Value to set for the given key. This will overwrite any existing value, if the key
            already exists.

        Raises
        ------
        ValueError
            If the message is null/empty, the message contents cannot be set
        """
        if not self:
            raise ValueError("Cannot set the message contents for a null message")
        else:
            self._content[key] = value

    def sender(self) -> Optional[int]:
        """Get the ID (32-bit integer) of the robot that sent the message

        Returns
        -------
        int or None
            ID of the sending (transmitting) robot
        """
        return self._tx_id

    def __bool__(self) -> bool:
        return not self._is_null

    def __str__(self) -> str:
        """
        Format the message as a human-readable string

        Returns
        -------
        str
            Friendly message format (or says it's an empty message)
        """
        if self._is_null:
            return "NULL message"
        else:
            return f'{self._tx_id} -> {self._rx_type}: {self._content}'
