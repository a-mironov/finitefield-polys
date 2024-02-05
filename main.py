import polynomial

exitflag = False
# warning flag for setchar
charflag = False

welcomemsg = "Welcome to Finite Field Polynomial Calculator!"
print(welcomemsg)

## command help messages
cmds_list = {}
# meta commands
cmds_list["exit"] = """Usage: exit\n
Exits the program."""
cmds_list["help"] = """Usage: help <cmd>\n
Prints a description of its input command. Ignores subsequent arguments."""
cmds_list["list"] = """Usage: list\n
Lists all currently supported commands."""
# initialization commands
cmds_list["setchar"] = """Usage: setchar <number>\n
Sets the base field characteristic to `number`. If this causes a change,
all stored polynomials are deleted! Warns the user before proceeding."""
cmds_list["char"] = """Usage: char\n
Displays the current characteristic of the base field."""
# data management commands
cmds_list["create"] = """Usage: create <name> <coeffs>\n
Creates a polynomial by name `name` with coefficients `coeffs`, read in ascending order of degree."""
cmds_list["show"] = """Usage: show <name>\n
Displays the polynomial by name `name` (if it exists) on the screen."""
cmds_list["showall"] = """Usage: showall\n
Displays all currently stored polynomials on the screen."""
cmds_list["delete"] = """Usage: delete <name>\n
Deletes the polynomial by name `name`."""
cmds_list["update"] = """Usage: update <name> <coeffs>\n
Updates the polynomial by name `name` with new coefficients <coeffs>."""
# arithmetic commands
cmds_list["add"] = """Usage: add <name1> <name2> <result>\n
Adds the polynomials by names `name1` and `name2` and stores the result in `result`. `name1` and `name2` must exist, while `result` must not exist."""
cmds_list["subtract"] = """Usage: subtract <name1> <name2> <result>\n
Subtracts the polynomials by names `name1` and `name2` and stores the result in `result`. `name1` and `name2` must exist, while `result` must not exist."""
cmds_list["multiply"] = """Usage: multiply <name1> <name2> <result>\n
Multiplies the polynomials by names `name1` and `name2` and stores the result in `result`. `name1` and `name2` must exist, while `result` must not exist."""


cmd = ""
while not exitflag:
    # if last command was not setchar, clear the flag
    if cmd != "setchar":
        charflag = False
    ## input processing
    # raw user input
    userin = input("> ")
    
    # clean up duplicate spaces in user input
    # join and re-split...
    userin_clean = " ".join(userin.rstrip(" ").split())
    args = userin_clean.split(" ")
    cmd = args[0]
    argc = len(args) - 1
    # all data-mgmt commands have name as their first argument
    if argc > 0:
        name = args[1] 

    ## commands processing
    match cmd:
        case "setchar":
            if not charflag:
                print(f"""Warning! Changing the characteristic will delete all
stored polynomials! Repeat the command to confirm.""")
                charflag = True
                continue
            else:
                try:
                    new_char = int(args[1])
                except ValueError:
                    print(f"Could not parse {args[1]} as an integer!")
                else:
                    try:
                        polynomial.set_characteristic(new_char)
                    except ValueError as e:
                        print(e)
                    else:
                        print(f"Characteristic set to {new_char} successfully.")
                        charflag = False
        case "char":
            print(f"Field characteristic is {polynomial.FCH}.")
        case "exit":
            print("Goodbye.")
            exitflag = True

        case "help":
            # if user typed only "help", return desc for help itself
            if argc == 0:
                print(cmds_list["help"])
            elif args[1] in cmds_list.keys():
                print(cmds_list[args[1]])
            else:
                print(f"Unrecognized command: {args[1]}!")
        case "list":
            print("Available commands:")
            for command in cmds_list.keys():
                print(command)
        case "create":
            try:
                polynomial.make_poly(name, args[2:])
            except ValueError as e:
                print(e)
            else:
                print(f"Polynomial {name} created.")
        case "show":
            try:
                display_string = polynomial.display_poly(name)
            except KeyError as e:
                name = e.args[0]
                print(f"No polynomial by name {name} to print.")
            else:
                print(display_string)
        case "showall":
            if len(polynomial.poly_dict.keys()) == 0:
                print("No polynomials currently stored.")
            else:
                print(polynomial.display_all())
        case "delete":
            try:
                polynomial.del_poly(name)
            except KeyError as e:
                name = e.args[0]
                print(f"No polynomial by name {name} to delete.")
            else:
                print(f"Polynomial {name} deleted.")
        case "update":
            try:
                polynomial.update_poly(name, args[2:])
            except KeyError as e:
                name = e.args[0]
                print(f"No polynomial by name {name} to update! "+
                      "Use `create` to create new polynomials.")
            else:
                print(f"Polynomial {name} updated.")
        case "add":
            try:
                polynomial.addmake_poly(args[1], args[2], args[3])
            except ValueError as e:
                print(e)
            except KeyError as e:
                name = e.args[0]
                print(f"Polynomial {name} not found!")
            else:
                print(f"Sum {args[1]}+{args[2]} stored in {args[3]}.")
        case "subtract":
            try:
                polynomial.submake_poly(args[1], args[2], args[3])
            except ValueError as e:
                print(e)
            except KeyError as e:
                name = e.args[0]
                print(f"Polynomial {name} not found!")
            else:
                print(f"Difference {args[1]}-{args[2]} stored in {args[3]}.")
        case "multiply":
            try:
                polynomial.mulmake_poly(args[1], args[2], args[3])
            except ValueError as e:
                print(e)
            except KeyError as e:
                name = e.args[0]
                print(f"Polynomial {name} not found!")
            else:
                print(f"Product {args[1]}*{args[2]} stored in {args[3]}.") 
        case _:
            print(f"Unknown command: {cmd}!")
