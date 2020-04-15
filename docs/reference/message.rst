Message
=======

This provides a basic Message protocol for robot communication. Each message contains the ID of the sender and a dictionary of message contents. The values of the message contents may be any type, so the receiver must know how to process the data.

Additionally, Messages can optionally include a receiver type (``rx_type``). This is only needed if there are multiple types of robots in the World, and you only want certain types of robots to receive the message.

If no arguments are provided when a Message is created, it creates a null message, which signals that the robot is not broadcasting anything.

While it is possible to extend this class, the default Message class should meet most needs.

.. autoclass:: gridsim.message.Message
    :members: