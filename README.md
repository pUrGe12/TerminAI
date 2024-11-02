# TerminAI

<p align="center">
  <img src="https://img.shields.io/badge/Code-Python-informational?style=flat&logo=python&color=blue" alt="Python" />
  <img src="https://img.shields.io/badge/Code-Bash-informational?style=flat&logo=Bash&color=yellow" alt="bash" />
</p>

**A terminal with AI capabilities.** Forget commands, just tell it what it do! 

> [!IMPORTANT]
> A step towards **AIOS**.

Check out the terminal [here](./terminal_gui/README.md)!

## The structure

For a better understanding of the structure refer the [workflow](./idea/README.md)

This is the basic architecture, it is not very precise. The more detailed ones will be present in the respective directories.

![Architecture](./idea/TerminAI.png)

---

> [!IMPORTANT]
> Complete means, in a ready to work **right now** condition.

Pending work:

- [x] Write the workflows properly. Don't leave anything ambiguous.
- [ ] Complete [sequencer](./Sequencer). The pending work will be listed there.
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
2. You will receive a `URL` and a `key`. Place those in [sequencer](./Sequencer/sequencer.py) in the approriate spot (it has been demarcated for you).
3. Create a table with the name `History`.

And you're good to proceed.

### Adding API keys

To run the models you will need an API key. 

1. Here over to [google gemini](https://ai.google.dev/gemini-api/docs/api-key) and get your API key.
2. Place your API key in the [API keys file](./extraction_models/APIKEYS.py). The exact spot has been demarcated for you.

And you're good to go!

---