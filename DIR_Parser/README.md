# Directory structure analyser

This is the directory parser, this will understand the current directory system (hopefully pretty fast) and store it in a relevant format. It's not going to read your files, its just going to read the entire directory format, as in, how your laptop is structured.

It will read that, and then use it to perform file operations.


## Goals

- [ ] It is able to parse every directory and store the names it in a json format.

For example, 

		{
		"/" : "home", "bin", "usr", "dev" ...
		"home": "purge"
		"purge": "Desktop", "Downloads", ".cache", ...
		...
		...
		}


- [ ] We make multiple copies of this. The main copy is similar to the one shown above, there are also smaller copies. These copies are essentially seperated directory wise.

So, we take each element of the main copy, and expand it's directory structure only. This is to increase modularity, in case the code only needs a specific directory structure. 

- [ ] Able to provide the necessary structure to the model that demands it.

This I will have to see, on how exactly we can provide these to the exact models.