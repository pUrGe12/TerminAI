# The structure

We need to have a `setup` too! This setup should take in values from the user's laptop, the directory structure, to understand what all directories exist, what all files exist and all. 

This must be automatic! Preferrably a bash script that will read the directory structure and store the relevant information in a file or a database.

This file/database must then be called by the models to make better judgements.

## Brief explantion of the Idea

1. The user is expected to enter something like "write a 500 word essay on Abraham Lincon in a file in my desktop".

2. The user's prompt is sent first to the [backend_endpoint](./Backend_endpoit). This is a breakout, where it receives message to send to the user, and forwards the user's prompt for further processing.

3. Now comes the sequencer. This will broadcast the message to all the models in the extraction layer. These are many in number and they are extracting what exactly the user wants, in broad terms. 

I am thinking 6 extraction models,

    file operations (opening, writing to a file, creating a directory)
    operating system operations (changing brightness, killing processes, changing permissions)
    application level operations (starting a browser, searching for a specific thing, closing a certain software, using a specific software)
    network level operations (switching wifi bluetooth on and off, checking connected devices via USB)
    installing operations (new software, pip installs, sudo apt-gets)
    content generation operations (any content that needs to be printed on the terminal, printed on terminal being important here. For example, greetings.)

These are broad and cover most of the use cases.

4. In this case, the expected output is from 1 model, `file operations` detector. This will give sysbool as `True`. It will give a summary as well, and the function name gives the type of detection it was performing.

5. This will be sent to the sequencer as the feedback to add to the database. 

6. This will also be sent to the breakout GPT. This will figure out which GPT model to send the data to based on where it is coming from. `File operations` will have its own smaller GPT models, and this will figure out where to send what. 

7. The smaller GPT models will basically try to generate a json type object of the necessary parameters, to fulfill the request and see which parameters are missing. The missing ones, they'll add on their own. 

Note that they will have the help of the setup_config file which contains the directory structure and the necessary names to generate perfect commands (This will be more relevant in the future).


> [!IMPORTANT]
> The breakout will broadcast this message to a certain group of ports, specific for file operations, like read, write, delete, touch, change permissions etc. There are many. The relevant ones respond with a 'yes' and therein lies bash scripts or `os commands`, whichever is more convinent that they can run based on what they do.

In this case, the write will fire up, which will create a json object containing where to write and what to write. Then the functions inside, will actually do that.

The model will then send this json object to model S, it will have a comprehensive history of what all has happened till now, and Model S will create a wrapper around it, beautify it and present it to the user.

8. If 2 extraction models fire up (which won't be very uncommon) then both of them will send for the breakout and the breakout will figure out where to forward each message based on where it came from (that is, what the original function's function was...)

Then, each will create a json object, and send that to the Model S.

What if they are dependent on each other? What if we have to write to a value that the other finds? 

For this we have a `concatenation model`. All json passes through the concatenation model, which looks at them all, judges if they are to be concatenated and does that (note that, the json contains the "value" that the model found, if it found anything at all). It has code to concatenate them. It will usually be do something, then based on that do something else. If there are more than 2, then we just tell the user to fuck off (for now...).

or we don't have to hardcode at all, we'll have a python file that has functions extensively written to perform different tasks. We will import this file and take the relevant functions.

> [!TIP]
> I am now thinking, what if we give broadcast the json to the smaller models, have the relevant one further refine it and then generate a command to do that? It will know exactly what the computer structure is from the config file... So, it will get the directory names right as well. Then we'll just execute it...

---


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