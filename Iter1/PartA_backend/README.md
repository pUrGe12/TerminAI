# Part A

This is the first half of the process. The following image will clarify exactly what is happening in this half. 

![backend part A](./images/PART_A_BACKEND.png)

---

> [!IMPORTANT] 
> To start

> Run the backend endpoint first

		python3 ./Backend_endpoint/commsBack.py

> Run the terminal 

		python3 ./terminal_gui/termEMU.py

> Run the sequencer

		python3 ./Sequencer/sequencer.py

---

## Potential issues

- [ ] Check in the `main` function, if the self.message_queue.get(timeout=5) is waiting for completion rather than broadcasting the data it gets right away.

> fix? We'll see about that later.

--- 

> [!NOTE]
> Running the clients won't work because you will first need to run the GPT Breakout code.

---