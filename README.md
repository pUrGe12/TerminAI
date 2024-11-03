# TerminAI

<p align="center">
  <img src="https://img.shields.io/badge/Code-Python-informational?style=flat&logo=python&color=blue" alt="Python" />
  <img src="https://img.shields.io/badge/Code-Bash-informational?style=flat&logo=Bash&color=yellow" alt="bash" />
</p>

**A terminal with AI capabilities.** Forget commands, just tell it what it do! 

> [!IMPORTANT]
> A step towards **AIOS**.

Check out the terminal [here](./terminal_gui/README.md)!

## Brief explantion of the Idea

1. The user is expected to enter something like "write a 500 word essay on Abraham Lincon in a file in my desktop".

2. The user's prompt is sent first to the [backend_endpoint](./Backend_endpoit). This is a breakout, where it receives message to send to the user, and forwards the user's prompt for further processing.

3. Now comes the sequencer. This will broadcast the message to all the models in the extraction layer. These are many in number and they are extracting what exactly the user wants, in broad terms. 

I am thinking 5 extraction models,

    file operations (opening, writing file etc)
    operating system operations (changing brightness, killing processes, changing permissions)
    application level operations (starting a browser, searching for a specific thing, closing a certain software, using a specific software)
    network level operations (switching wifi bluetooth on and off, checking connected devices via USB)
    installing operations (new software, pip installs, sudo apt-gets)

These are broad and cover most of the use cases.

4. In this case, the expected output is from 1 model, `file operations` detector. This will give sysbool as `True`. It will give a summary as well, and the function name gives the type of detection it was performing.

5. This will be sent to the sequencer as the feedback to add to the database. 

6. This will also be sent to the breakout GPT. WHAT HAPPENS HERE? 

---
IS THIS NEEDED??
---
### The wait logic

Here, in all models in the GPT layer we add a code to add to a database whatever they find, as soon as they're done executing (that is, if they answer 'yes' then it means its their job, and once they're done processing, we'll add it to a database).

We'll add the following things to the database.

- GPT model's function
- Time-stamp
- Value
- work-summary

What all this means? The `value` is the explicit thing that it computes. In this case, it will be the name of the file. It can be either something the user mentioned or didn't or something that the user wants to be computed. Each model has its own `value` to add in the `value` field. It's different things for all, but its something that piece of code computes. 

The `work-summary` is just a short message explaining what the model did.

As soon as they receive the broadcasted message, all models begin querying the `time-stamp` of the last added field in the database, at an interval of 1 second (can be changed). If the `current-time` - `time-stamp` is around 1 second (we can change this value in the future), then it implies that a model has just finished execution.

In this case, the content generation model needs the name of the file and the directory to write content into, this will be present in the value field. It will query that, and write to it.

It will then add its own entry in the database.

In this case, two models will report 'yes' in the GPT layer (yes as in, yes its their job). First will be the one that detects writing of a file. 

8. With this, the system level change has been executed. 

Each model is expected to send a message to the `Model S`. This is to ensure that all changes have been made and now we can generate the prompt that needs to be shown to the user. 

- `Model S` first checks who the sender is. If the sequencer is the sender, then we must be in the `b` part and hence, it generates the required content and sends it to the breakout, which then sends it back to the terminal.

- If sequencer is not the sender, then there must have been a system change (not necessarily part `a` cause even if its not a file input, all processes will eventually reach there). It means, the output is coming from the GPT layer.

If the model's output is 'yes' (recall the 'yes' and 'no' in the extraction models, similar concept), then it will first process, then send a 'done' message to Model 
S, and if 'no' then it will immediately send a 'done' message to Model S. This means, once Model S has the approriate number of 'done's it can start processing. 




## The structure

For a better understanding of the structure refer the [workflow](./idea/README.md)

This is the architecture.

![Architecture](./idea/TerminAI.png)

---

> [!IMPORTANT]
> Complete means, in a ready to work **right now** condition.

Pending work:

- [x] Write the workflows properly. Don't leave anything ambiguous.
- [x] Complete [sequencer](./Sequencer). The pending work will be listed there.
- [ ] Figure out the small part of sending GPT layer data in history is required or not.
- [ ] Complete [endpoint](./Backend_endpoint). The pending work will be listed there.  
- [ ] Complete [breakoutGPT](./BreakoutGPT). The pending work will be listed there.
- [ ] Write all extraction models. This will take some time.
- [ ] Complete GPT layer.

one more thing,

- [ ] Add links to [workflow](./idea/README.md) and make it readable.

---

## Installing

To install the necessary dependencies, use the following command

    pip install -r requirements.txt

Since, I don't have a huge database, you will need to set up your own in [supabase](https://supabase.com/). This better because now its fully personalised for you.

### Steps to setup the database

1. Head over to [supabase](https://supabase.com/). Create a new project.
2. You will receive a `URL` and a `key`. Place those in [API Keys file](./Sequencer/api_keys.py) in the approriate spot (it has been demarcated for you).
3. Create a table with the name `History`.

And you're good to proceed.

### Adding API keys

To run the models you will need an API key. 

1. Here over to [google gemini](https://ai.google.dev/gemini-api/docs/api-key) and get your API key.
2. Place your API key in the [API keys file](./extraction_models/api_keys.py). The exact spot has been demarcated for you.

And you're good to go!

For modularity's sake, you may wish to add these keys in [the home](./api_keys.py) API file as well. :smile:

---

## PART A

Check out [part A](./PartA_backend). This is essentially the main communcations part. The exact sequence is present in that respective directory

For an understanding of the communications in Part A, refer the [workflow](./PartA_backend/workflow.md)

---