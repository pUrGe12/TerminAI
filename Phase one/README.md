# Part A

This is the first part of the backend. Here is what it is able to do.

- [x] Have a [terminal](./terminal_gui) GUI, that can take user's prompts and display the responses.
- [x] Have an [endpoint] which will receive the user's message from the terminal and send out responses.

The endpoint will not receive the data from the `Model S` as of now.

- [x] The endpoint will forward the user's prompt to the [sequencer](./Sequencer).

The sequencer will do the following.

- [x] It will receive the user's prompt from the endpoint.
- [x] It will query the supabase table for history. Fields to be queried are `system_bool`, `extraction_model_function`, `prompt`, `extraction_model_summary`. These are what happened before.
- [x] It will then add the current prompt with this `history` and broadcast it (simultaneously) to the 6 models in the `extraction layer`.

- [x] It will then wait for their feedback. The feedback will include, `system_bool`, `extraction_model_function`, `extraction_model_summary` for the current prompt.

- [ ] It will then add the feedback along with the current prompt to the database for future history implementation. 

>[!TIP]
> Haven't tested this yet

- [ ] The extraction models will recieve the broadcast and start acting. 

>[!TIP]
> Haven't tested this yet

- [x] They will have 2 models running, one detects if the extraction that this file is going to do is what the prompt demands or not, and the other will actually perform.
- [x] The extraction performed outputs a json object that includes `model name` (so, we know what it was trying to do), some other important values. We'll leave it upto the model to detemine what `important` things it wants to include in the json. 

>[!TIP]
> Haven't tested this yet

- [ ] After having generated the json, we broadcast this json to the breakout.
- [ ] We also provide the feedback features to the sequencer again.