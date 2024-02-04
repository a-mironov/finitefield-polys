exitflag = False

welcomemsg = "Welcome to Finite Field Polynomial Calculator!"
print(welcomemsg)

cmds_list = {}
cmds_list["echo"] = """Auxiliary command.
Prints all of its arguments on the screen."""
cmds_list["exit"] = "Exits the program."
cmds_list["help"] = """Usage: help <cmd>\n
Prints a description of its input command. Ignores subsequent arguments."""


while not exitflag:
    ## input processing
    # raw user input
    userin = input("> ")
    # clean up duplicate spaces in user input
    userin_clean = " ".join(userin.rstrip(" ").split())
    args = userin_clean.split(" ")
    cmd = args[0]
    argc = len(args)-1

    ## commands processing
    ## eventually all logic should be redirected to modules
    ## and from here they will only be called
    # self-explanatory
    if cmd == "exit":
        print("Exiting...")
        exitflag = True
        continue
    # debug command, to be removed in final ver
    elif cmd == "echo":
        for i in range(1, argc+1):
            print(f"Argument {i}: {args[i]}")
        continue
    # no command recognized
    else:
        print(f"Unknown command: {cmd}!")
        continue
