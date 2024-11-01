# Explanation

Here is the exact explanation, point to point details, of what is happening with the sequencer.


:heavy_check_mark:  It has a socket connection with the breakout. It recieves user's prompt from there. It only needs to receive from the breakout and not send anything back.

:heavy_check_mark:  It broadcasts the user's input to all the models, at the same time.

:heavy_check_mark:  Establishes a listener thread for incoming messages from the models.

The models have been coded to reply if and only if they satisfy what is being asked. So, for any given prompt, there will only be one reply.
