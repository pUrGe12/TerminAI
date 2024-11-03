# Functionality

This is the breakout for comms between extraction layer and the GPT layer.

- [x] Establish comms with extraction layer
- [ ] Establish comms with GPT layer

This is able to receive the following from the extraction layer,

1. Which model fired up --> Tell's what they were looking for using `address.py`
2. The system boolean value.
3. The user's prompt.

Now, here lies the logic which sends it to the relevant parts of the GPT layer.


> [!IMPORTANT]
> If it is a system level change, then the models need to know that there are other models also working on the same prompt, and they must wait their turn.

