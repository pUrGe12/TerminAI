# Explanation

This part of the structure is mostly communications. Here is an outline of what that means.

---

:zap: The terminal sends and receives data from the `endpoint`.

:hammer: The endpoint sends the user's prompt to the `sequencer`, while waiting for the response from `Model S`. After getting a response from `Model S` it sends that to be printed, while the system level changes are performed. The response is catered to that.

:mega: The sequencer recieves the message from the endpoint, adds to that the history then broadcasts it for all the models to hear. It then waits for their feedback which it adds to the `history database`. It does not send any back data to the endpoint.

---

The models will then process it, and send the output to the breakout. The breakout will do the filtering and send it to the relevant model in the GPT layer. The GPT layer does the response generation and figuring out the system level changes.