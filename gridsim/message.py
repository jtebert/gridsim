# from __future__ import annotations  # For the type checking circular import

from typing import Dict, Any, Optional, Type  # , TYPE_CHECKING

from .robot import Robot

# if TYPE_CHECKING:
#     from .robot import Robot


class Message:
    def __init__(self, tx_id: Optional[int] = None,
                 content: Dict[str, Any] = {},
                 rx_type: Type[Robot] = Robot,  # Default is any robot
                 ):
        """
        A message sent by robots. Can be either a null (empty) message if no
        arguments are provided to the constructor. Or it contains the sender's
        ID, a dictionary of content, and (optionally) the type of robot that
        receives the message.

        Parameters
        ----------
        tx_id : Optional[int], optional
            ID of the sending (transmitting) robot, by default None
        content : Dict[str, Any]] optional
            Dictionary of message keys and values, by default an empty
            dictionary. Keys must be strings, but values can be of any type
            (incumbent on receiver to correctly interpret incoming data)
        rx_type : Type[Robot], optional
            Type of the receiving robot, by default Robot (i.e., message will be
            processed by any Robot.)
        """
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
        """
        Get the contents of the message

        Parameters
        ----------
        key : Optional[str], optional
            Name of the parameter to retrieve, by default None. If not
            specified, a dictionary of all parameters will be returned.

        Returns
        -------
        Optional[Dict[str, Any]]
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

    def sender(self) -> Optional[int]:
        """
        Get the ID (32-bit integer) of the robot that sent the message

        Returns
        -------
        Optional[int]
            ID of the sending (transmitting) robot
        """
        return self._tx_id

    def __bool__(self) -> bool:
        return not self._is_null

    def __str__(self) -> str:
        """Format the message as a human-readable string

        Returns
        -------
        str
            Friendly message format (or says it's an empty message)
        """
        if self._is_null:
            return "NULL message"
        else:
            return '{id} -> {type}: {contents}'.format(
                id=self._tx_id,
                type=self._rx_type,
                contents=self._content
            )
