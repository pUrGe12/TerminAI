# Sequencer

Functionality

- [x] Broadcast user's message to all clients.
- [x] Receive feedback, that is, which model fired up and what the response was.
- [x] The feedback to be received is, `system boolean value`, `model function`, `work summary`. The prompt will be present with the sequencer. 

Model function is actually decoded in the sequencer code itself, through the sender's name. (for no particular reason)

> [!NOTE]
> The response will either be a binary or a tertiary, no more that than.

- [x] Connect to supabase and push the feedback, along with the prompt. It is able to push the `system_boolean`, `ex_model_function`, `user_prompt`, `ex_work_summary`.
- [x] Before broadcasting, pull from relevant data from the database and add that to the user's message, explicitly mentioning it as `history`. 

- [ ] Handle more than one responses from the extraction layer (that is, added all to the database).

> [!IMPORTANT]
> The sequencer will not send anything back to the breakout. The final response will be recieved by the `Model S`.

---

The sequencer is the main part of the problem, responsible for `establishing communications` between the client and all the models.

![Sequencer workflow](./images/Sequencer.png)

---

What works:

- [x] Broadcaster is able to query the database and send history.
- [x] The client is able to receive history and the prompts.
- [x] The client gets the right things from history.
- [x] The broadcaster is able to add to the database based on the response from the client.
- [x] Establish comms with [endpoint](../Backend_endpoint/commsBack.py)

---

- [x] History fixed. The logic is now to wait for 5 seconds for a response before checking if the `message_queue` is empty or not. 

Before, it used to immediately do that, hence always resulting in an empty queue. If we receive a message within these 5 seconds, then we immediately proceed forward.

---