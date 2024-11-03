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

A potential solution is this. Going over it step by step:

1. Every model has been broadcasted the prompt, the sysbool value and all.

2. All models will begin processing at roughly the same time.

3. The model that finishes and answer's `yes` (to its finishing) will be allowed to add the "value" along with a "timestamp", "model name" and a "work_summary" to a database.

The `model name` gives what the model was doing (that is, its functionality), and the `time-stamp` is important because

- [x] The model that finishes first, does its work, gives a short summary of what it did in 20 words (this is the "work_summary") and the important values it generated (this is the "value") 

> [!NOTE]
> This will necessarily be the model that could run given the bare prompt, and is not dependent on the output of other models.

- The `value` will depend on what the model was doing and it may not be needed all the time. This is something we can control by telling each model what to output or something.

- The models which are dependent on the output of others will have to do this

- [x] The other models continually query the time-stamp of the database's last entry, at intervals of 1 second , compare it to the current time. If the difference between them is around 1 second, that means some other model just finished execution!

It will then use that value and finish its own execution.

5. To send the data to model s, 

- Count the total output you got (yes's and no's), if the number equals total number of models, then you can query the database and send the value and the summary to the model S.