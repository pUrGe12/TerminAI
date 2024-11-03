# The structure


## Frontend

1. A terminal display that is presented to the user, created using GUI tools from python.

2. This terminal communicates via web-sockets to the backend which is listening attentively. The user enters some input and this is sent to the backend.

3. The extraction layer also let's the sequencer know which model has been activated. 
---

## Backend

1. The input passes through a sequencer, or basically through every extraction model in parallel. 

The extraction models are there to figure out what the user wants exactly. They don't perform the task required by themselves, just figure out what to perform. 

Each model caters to one specific bucket of tasks. For example, the task can be to open a file, in which case one extraction model will activate and give a positive response, while all others give a negative response. 

"I want to know about the blue hornbilled koala" -> The model that detects no system change and general information will get activated.

2. All extraction models will give an output, and these outputs will be given to another set of GPT models.

The GPT models perform the actual task of content generation (if that is the required case as in "I want to know about the blue hornbilled koala") or system level changes. 

In short, each extraction model is linked to a specific GPT model. If that extraction model ignites, then its linked GPT model will activate and do the task.

This linkage is performed via a breakout.

For system level changes, they basically "call" in some sense a function that does that. I am thinking bash or python, either works, but the idea is,
 
- We'll have different files for performing different system level tasks (these can be bash scripts or python scripts, either works)

- When the extraction models complete their work, the one that gave a positive output will send it to the relevant GPT model. The GPT model (which is a python script) will import the necessary file to perform the system level function (if required) and execute that.

It will be pretty comprehensive and a lot of functions will be needed but that's how it is.

3. Again, only one GPT model fires at a time, and none other gives any output. (we need to keep others dormant which is doable cause they're all different python files).

4. The output goes to the Model S (Supreme model), which wraps the output around a general human-like response. 

For example, if there was a system level task, it will give what all changes were made, what problems were faced etc. like a general human would.

5. The output of Model S is communicated back to the Terminal GUI via web-sockets and shown to the user. 

---

# The important bits

We'll be using some light-weight models in the extraction layers, and LLMs like gemini or ChatGPT for the GPT layer. The main thing is to keep execution parallel, cause else, it will be very slow and you don't want that. 

## How will parallel execution work?

Use a broadcaster, and broadcast the message so that each model picks it up at relatively the same time.