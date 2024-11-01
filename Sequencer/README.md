# Sequencer

Functionality

- [x] Broadcast user's message to all clients.
- [x] Receive feedback, that is, which model fired up and what the response was.

> [!NOTE]
> The response will either be a binary or a tertiary, no more that than.

- [x] Connect to supabase and push the feedback.
- [x] Before broadcasting, pull from database and add that to the user's message, explicitly mentioning it as `history`.

> [!IMPORTANT]
> The sequencer will not send anything back to the breakout. The final response will be recieved by the `Model S`.

---

The sequencer is the main part of the problem, responsible for `establishing communications` between the client and all the models.

![Sequencer workflow](./images/Sequencer.png)

---

What works so far:

- [x] Broadcaster is able to query the database and send history
- [x] The client is able to receive history
- [x] The client gets the right things from history (that is, the GPT doesn't need ID and all)
- [x] The broadcaster is able to add to the database based on the response from the client
- [ ] Establish comms with breakout

---

- [x] History fixed. The logic is now to wait for 5 seconds for a response before checking if the `message_queue` is empty or not. 

Before, it used to immediately do that, hence always resulting in an empty queue. If we receive a message within these 5 seconds, then we immediately proceed forward.