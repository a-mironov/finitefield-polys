import polynomial
import parith

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
cmds_list["copy"] = """Usage: copy <src> <dest>\n
Copies the polynomial by name `src` into `dest`. Warning: This command overwrites the polynomial by name `dest` if present!"""
cmds_list["rename"] = """Usage: rename <oldname> <newname>\n
Renames a polynomial from `oldname` to `newname`."""
# arithmetic commands
cmds_list["add"] = """Usage: add <name1> <name2> <result>\n
Adds the polynomials by names `name1` and `name2` and stores the result in `result`. `name1` and `name2` must exist, while `result` must not exist."""
cmds_list["subtract"] = """Usage: subtract <name1> <name2> <result>\n
Subtracts the polynomials by names `name1` and `name2` and stores the result in `result`. `name1` and `name2` must exist, while `result` must not exist."""
cmds_list["multiply"] = """Usage: multiply <name1> <name2> <result>\n
Multiplies the polynomials by names `name1` and `name2` and stores the result in `result`. `name1` and `name2` must exist, while `result` must not exist."""
cmds_list["lincomb"] = """Usage: lincomb <weight1> <poly1> [<weight2> <poly2> [...]] <result>\n
Computes a scalar linear combination of the indicated polynomials and stores the result in `result` (which must not exist)."""
cmds_list["power"] = """Usage: power <basename> <exponent> <result>\n
Raises the polynomial by name `basename` to the power specified by the exponent, and stores the result in `result` (which must not exist)."""
cmds_list["eucdiv"] = """Usage: eucdiv <dividend> <divisor> <quotient> <remainder>\n
Performs Euclidean division and stores the results (quotient and remainder) under their indicated names (which must not exist)."""


def parse_lincomb(arguments: list):
    """
    parses argument list for `lincomb` command
    assumes the last argument (`result`) is NOT present, i.e. only inputs
    attempts to parse arguments as alternating weights and polynomials
    """
    if len(arguments) % 2 == 1:
        raise ValueError(f"Invalid argument count -- expected an even number, read {len(arguments)}.")
    
    weights = []
    polynames = []
    for i in range(len(arguments)):
        # even positions expect weights
        if i % 2 == 0:
            try:
                weights.append(int(arguments[i]))
            except ValueError:
                raise ValueError(f"Could not parse {arguments[i]} as integer")
        else:
            name = arguments[i]
            if name not in polynomial.poly_dict.keys():
                raise KeyError(name)
            polynames.append(name)
    return (weights, polynames)


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
        # initialization & meta commands
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
            for command in sorted(cmds_list.keys()):
                print(command)
        # data management commands        
        case "create":
            if argc == 0:
                print("Too few arguments!")
                print(cmds_list[cmd])
                continue
            try:
                polynomial.make_poly(name, args[2:])
            except ValueError as e:
                print(e)
            else:
                print(f"Polynomial {name} created.")
        case "show":
            if argc == 0:
                print(cmds_list[cmd])
                continue
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
            if argc == 0:
                print(cmds_list[cmd])
                continue
            try:
                polynomial.del_poly(name)
            except KeyError as e:
                name = e.args[0]
                print(f"No polynomial by name {name} to delete.")
            else:
                print(f"Polynomial {name} deleted.")
        case "update":
            if argc == 0:
                print(cmds_list[cmd])
                continue
            try:
                polynomial.update_poly(name, args[2:])
            except KeyError as e:
                name = e.args[0]
                print(f"No polynomial by name {name} to update! "+
                      "Use `create` to create new polynomials.")
            else:
                print(f"Polynomial {name} updated.")
        case "copy":
            if argc < 2:
                print("Too few arguments!")
                print(cmds_list[cmd])
                continue
            try:
                polynomial.copy_poly(args[1], args[2])
            except KeyError as e:
                name = e.args[0]
                print(f"No polynomial by name {name} to copy.")
            else:
                print(f"Polynomial {args[1]} copied to {args[2]}.")
        case "rename":
            if argc < 2:
                print("Too few arguments!")
                print(cmds_list[cmd])
                continue
            try:
                polynomial.rename_poly(args[1], args[2])
            except KeyError as e:
                name = e.args[0]
                print(f"No polynomial by name {name} to rename.")
            except ValueError as e:
                print(e)
            else:
                print(f"Polynomial {args[1]} renamed to {args[2]}.")
        # arithmetic commands        
        case "add":
            if argc < 3:
                print("Too few arguments!")
                print(cmds_list[cmd])
                continue
            try:
                parith.addmake_poly(args[1], args[2], args[3])
            except ValueError as e:
                print(e)
            except KeyError as e:
                name = e.args[0]
                print(f"Polynomial {name} not found!")
            else:
                print(f"Sum {args[1]}+{args[2]} stored in {args[3]}.")
        case "subtract":
            if argc < 3:
                print("Too few arguments!")
                print(cmds_list[cmd])
                continue
            try:
                parith.submake_poly(args[1], args[2], args[3])
            except ValueError as e:
                print(e)
            except KeyError as e:
                name = e.args[0]
                print(f"Polynomial {name} not found!")
            else:
                print(f"Difference {args[1]}-{args[2]} stored in {args[3]}.")
        case "lincomb":
            if argc < 3:
                print("Too few arguments!")
                print(cmds_list[cmd])
                continue
            resultname = args[-1]
            if resultname in polynomial.poly_dict.keys():
                print(f"Cannot store linear combination in {result} -- name already in use.")
            else:
                try:
                    weights, polynames = parse_lincomb(args[1:-1])
                except ValueError as e:
                    print(e)
                except KeyError as e:
                    name = e.args[0]
                    print(f"Polynomial {name} not found!")
                else:
                    polys = []
                    for i in range(len(polynames)):
                        polys.append(polynomial.poly_dict[polynames[i]])
                    result = parith.lincomb(weights, polys)
                    polynomial.make_poly(resultname, result.coeffs)
                    print(f"Linear combination stored in {resultname}.")
        case "multiply":
            if argc < 3:
                print("Too few arguments!")
                print(cmds_list[cmd])
                continue
            try:
                parith.mulmake_poly(args[1], args[2], args[3])
            except ValueError as e:
                print(e)
            except KeyError as e:
                name = e.args[0]
                print(f"Polynomial {name} not found!")
            else:
                print(f"Product {args[1]}*{args[2]} stored in {args[3]}.")
        case "power":
            if argc < 3:
                print("Too few arguments!")
                print(cmds_list[cmd])
                continue
            try:
                parith.powmake_poly(args[1], int(args[2]), args[3])
            except ValueError as e:
                print(e)
            except KeyError as e:
                name = e.args[0]
                print(f"Polynomial {name} not found!")
            else:
                print(f"Power {args[1]}^{args[2]} stored in {args[3]}.")
        case "eucdiv":
            if argc < 4:
                print("Too few arguments!")
                print(cmds_list[cmd])
                continue
            try:
                parith.eucdivmake_poly(args[1], args[2], args[3], args[4])
            except ValueError as e:
                print(e)
            except KeyError as e:
                name = e.args[0]
                print(f"Polynomial {name} not found!")
            except ZeroDivisionError:
                print(f"Divisor {args[2]} cannot be zero!")
            else:
                print(f"Euclidean division of {args[1]} by {args[2]} completed.")
                print(f"Quotient and remainder stored in {args[3]} and {args[4]} respectively.")
        
        case _:
            print(f"Unknown command: {cmd}!")
