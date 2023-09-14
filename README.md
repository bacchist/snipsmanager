# Code Snippet Manager
#### Video Demo:  https://youtu.be/mw1xEp2YZ3M
#### Description:

This application works with JSON files containing vscode format code snippets. It accepts 4 commands: show-all, show, edit, and new. The show-all command displays an index of the contents of the snippet file in a nicely formatted table. The show command displays the "body" or actual code of the snippet. The edit command allows you to edit the body of a single snippet without disturbing the rest of the file. And finally, the new command lets the user interactively write a new snippet and add it to a file.

The primary motivation for the project came to me when I was trying to figure out what snippets were available to me after installing a new editor. The command to show the available snippets simply displayed raw JSON with no syntax highlighting or search functionality. I found it hard to separate the signal from all the noise and process it all. So I decided to write a script to display it on the screen in an easily digestible form.

I got a lot of mileage out of the [Typer](https://typer.tiangolo.com/) library, which I would come to find even more feature rich than I had first realized. This is in no small part due to the companion library [Rich](https://rich.readthedocs.io/en/stable/index.html#). Rich provided modules for printing tables, syntax highlighting, logging, and more. As I explored these libraries, I ended up reimplementing features to utilize them almost exclusively. Not that I was unhappy with the original implementations or the capabilities of the other libraries, but because it caused less friction and overhead, it ultimately resulted in fewer dependencies and more coherent code.

One of the biggest andvantages to Typer is its handling of commands, arguments, and options. All the approppriate checks and user feedback are baked in. The `@app.command()` decorator allows you to cleanly designate the entry point of the major features that your application offers. This allowed me to place almost all of the validation logic in a single function. That included JSONDecodeErrors in the event the input file was not valid JSON, as well as the presence of the fields that the rest of the application expects to find. There was only one edge case that I came across that had to be handled inside one of the other functions, which was due to the "body" of some entries containing strings, and others containing lists.

I used the standard library for logging to file, and Rich for logging to the console. I based this off of [an example](https://calmcode.io/logging/rich.html) I found of using multiple handlers. The only unrecoverable error that I am aware of is when the input file is invalid JSON, and the file can't be loaded. That is logged to stdout and to file and the program aborts. In the event of missing fields in an otherwise valid file, the occurrance is logged and that entry is disregarded, allowing the program to continue. For the show and show-all commands, they remain part of the file, as it is never modified. However, the edit and new commands result in the original file being written over without confirmation or warnings. That is something noted in the source as a TODO item. Hopefully that will be a priority if any work is done on this in the future.

Another loose end that I did not have time to address was my use of nvim to write/edit the body of snippets. This will clearly not work on many (or most) systems. This also happened to be an area where testing could be more robust as well. I was able to test that the subprocess was called, but it would be nice to verify user input in some way. Beyond that, work could continue to be done on this in order to add more features. A short list would be to add support for other snippets formats, editing of other elements aside from just the body, support for multiple files, deletion of snippets, and creation of a new file.

Whether or not I continue to develop this into a feature complete application, it was an excellent opportunity to explore Typer and Rich. I am sure to get a lot of mileage out of both in the future.
