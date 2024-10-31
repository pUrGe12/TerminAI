# Sequencer

Functionality

- [x] Broadcast user's message to all clients.
- [x] Receive feedback, that is, which model fired up and what the response was.

The response will either be a binary or a tertiary, no more that than.

- [ ] Connect to supabase and push the feedback.
- [ ] Before broadcasting, pull from database and add that to the user's message, explicitly mentioning it as `history`.

---

The sequencer is the main part of the problem, responsible for `establishing communications` between the client and all the models.

![Sequencer workflow](./images/Sequencer.png)

---

What works so far:

- [x] Broadcaster is able to query the database and send history
- [x] The client is able to receive history
- [ ] The client gets the right things from history (that is, the GPT doesn't need ID and all)
- [ ] The broadcaster is able to add to the database based on the response from the client
- [ ] Establish comms with breakout 

Write same code for all clients, change the GPT's prompt.

Run and fix history. If there can only be 1 element in the queue, cause we're getting then why am I seeing two? CHECK THE PIC.