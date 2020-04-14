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
        # Validate the message contents
        if tx_id is None and content is None:
            # Null message
            self._tx_id = None
            self._rx_type = None
            self._content = None
            self.is_null = True
        else:
            if not issubclass(rx_type, Robot):
                raise TypeError('Receiver type must be a subclass of Robot')
            if not isinstance(content, Dict) or \
                    not all(map(lambda k: isinstance(k, str), content.keys())):
                raise TypeError('Content must be a dictionary with string keys')
            else:
                self._tx_id = tx_id
                self._rx_type = rx_type
                self._content = content
                self.is_null = False

    def get(self) -> Optional[Dict[str, Any]]:
        # Retrieve the message contents
        return self._content
