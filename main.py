import polynomial
import parith

exitflag = False
# warning flag for setchar
charflag = False

welcomemsg = ("Welcome to Finite Field Polynomial Calculator!\n"+
              f"Default field characteristic is {polynomial.FCH}.\n"+
              "To set the characteristic, use the `setchar` command.\n"+
              "Type `list` for all available commands.")
print(welcomemsg)

## command help messages
cmds_list = {}
aliases = []
# general and initialization commands
cmds_list["exit"] = ("Usage: exit\n\n"+
                     "Exits the program.\n\n"+
                     "Alias: quit")
cmds_list["quit"] = ("Alias for `exit`.")
aliases.append("quit")
cmds_list["help"] = ("Usage: help OR help <cmd> OR help <n>\n\n"+
                     "With no input, prints the list of help pages.\n"+
                     "With a command, prints the description and usage "+
                     "for that command.\nWith a number, prints description "+
                     "and usage for all commands on that help page.")
cmds_list["list"] = ("Usage: list\n\n"+
                     "Lists all currently supported commands.")
cmds_list["setchar"] = ("Usage: setchar <number> [CONFIRM]\n\n"+
                        "Sets the base field characteristic to `number`. "+
                        "If this causes a change, all stored polynomials "+
                        "are deleted! Warns the user before proceeding.\n"+
                        "If second argument is present and equal to "+
                        "'CONFIRM', in all caps, without quotes, "+
                        "this command bypasses the warning.")
cmds_list["char"] = ("Usage: char\n\n"+
                     "Displays the current characteristic of the base field.")
# data management commands
cmds_list["create"] = ("Usage: create <name> <coeffs>\n\n"+
                       "Creates a polynomial by name `name` with "+
                       "coefficients `coeffs`, read in ascending order "+
                       "of degree.")
cmds_list["show"] = ("Usage: show <name>\n\n"+
                     "Displays the polynomial by name `name` (if it exists) "+
                     "on the screen.")
cmds_list["showall"] = ("Usage: showall\n\n"+
                        "Displays all currently stored polynomials on the screen.")
cmds_list["delete"] = ("Usage: delete <name>\n\n"+
                       "Deletes the polynomial by name `name`.")
cmds_list["deleteall"] = ("Usage: deleteall CONFIRM\n\n"+
                          "If the first argument is 'CONFIRM', in all caps, "+
                          "without quotes: deletes all stored polynomials. "+
                          "Otherwise, does nothing.\n\n"+
                          "Alias: flush")
cmds_list["flush"] = ("Alias for `deleteall`.")
aliases.append("flush")
cmds_list["update"] = ("Usage: update <name> <coeffs>\n\n"+
                       "Updates the polynomial by name `name` with new "+
                       "coefficients `coeffs`, read in ascending order "+
                       "of degree.")
cmds_list["copy"] = ("Usage: copy <src> <dest>\n\n"+
                     "Copies the polynomial by name `src` into `dest`. Warning: "+
                     "This command overwrites the polynomial by name `dest` "+
                     "if present!")
cmds_list["rename"] = ("Usage: rename <oldname> <newname>\n\n"+
                       "Renames a polynomial from `oldname` to `newname`.")
# arithmetic commands
cmds_list["add"] = ("Usage: add <name1> <name2> <result>\n\n"+
                    "Adds the polynomials by names `name1` and `name2` "+
                    "and stores the result in `result`. `name1` and `name2` "+
                    "must exist, while `result` must not exist.")
cmds_list["subtract"] = ("Usage: subtract <name1> <name2> <result>\n\n"+
                    "Subtracts the polynomials by names `name1` and `name2` "+
                    "and stores the result in `result`. `name1` and `name2` "+
                    "must exist, while `result` must not exist.\n\n"+
                    "Alias: sub")
cmds_list["sub"] = ("Alias for `subtract`.")
aliases.append("sub")
cmds_list["multiply"] = ("Usage: multiply <name1> <name2> <result>\n\n"+
                    "Multiplies the polynomials by names `name1` and `name2` "+
                    "and stores the result in `result`. `name1` and `name2` "+
                    "must exist, while `result` must not exist.\n\n"+
                    "Alias: mul")
cmds_list["mul"] = ("Alias for `multiply`.")
aliases.append("mul")
cmds_list["lincomb"] = ("Usage: lincomb <weight1> <poly1> "+
                        "[<weight2> <poly2> [...]] <result>\n\n"+
                        "Computes a scalar linear combination of the "+
                        "indicated polynomials and stores the result in "+
                        "`result` (which must not exist).\n\n"+
                        "Alias: lc")
cmds_list["lc"] = ("Alias for `lincomb`.")
aliases.append("lc")
cmds_list["power"] = ("Usage: power <basename> <exponent> <result>\n\n"+
                      "Raises the polynomial by name `basename` to power "+
                      "`exponent` and stores the result in `result` "+
                      "(which must not exist).\n\n"+
                      "Alias: pow")
cmds_list["pow"] = ("Alias for `power`.")
aliases.append("pow")
cmds_list["eucdiv"] = ("Usage: eucdiv <dividend> <divisor> <quot> <rem>\n\n"+
                       "Performs Euclidean division and stores the results "+
                       "(quotient and remainder) under their indicated names "+
                       "(which must not exist).")
cmds_list["eval"] = ("Usage: eval <name> <point>\n\n"+
                     "Evaluates the polynomial by name `name` at x = `point` "+
                     "and prints the value on the screen.")
cmds_list["modulo"] = ("Usage: modulo <name> <modulus> <result>\n\n"+
                       "Reduces polynomial `name` modulo polynomial "+
                       "`modulus` and stores the result in `result` "+
                       "(which must not exist).\n\n"+
                       "Alias: mod")
cmds_list["mod"] = ("Alias for `modulo`.")
aliases.append("mod")
cmds_list["eea"] = ("Usage: eea <poly1> <poly2> <gcd> <coe1> <coe2>\n\n"+
                    "Performs the extended Euclidean algorithm on "+
                    "polynomials `poly1` and `poly2`, finding their "+
                    "greatest common divisor and its Bezout "+
                    "coefficients. Stores the GCD under name `gcd`, "+
                    "and the coefficients under names `coe1` and `coe2`. "+
                    "All three output names must not exist.")

help_pages = [["exit","help","list","setchar","char"],
              ["create","show","showall","delete","update","copy","rename"],
              ["add","subtract","multiply","lincomb",
               "power","eval","modulo","eucdiv","eea"]]

special_help_msg = ("Type `list` to see all commands.\n"+
                    "Type `help <cmd>` to view the description of one command,"+
                    "or type `help <n>` to view descriptions for all commands "+
                    "in one of the following groups:\n\n"+
                    "1. General commands\n"+
                    "2. Data management commands\n"+
                    "3. Arithmetic commands")

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
                raise ValueError(f"Could not parse {arguments[i]} as integer!")
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
        # initialization & general commands
        case "setchar":
            if argc == 0:
                print("Enter new characteristic!")
                print(cmds_list[cmd])
                continue
            # bypass warning if 2nd arg is "CONFIRM"
            if argc >= 2 and args[2] == "CONFIRM":
                charflag = True
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
        case "exit" | "quit":
            print("Goodbye.")
            exitflag = True
        case "help":
            # if user typed only "help", return special help msg
            if argc == 0:
                print(special_help_msg)
            elif args[1] in cmds_list.keys():
                print(cmds_list[args[1]])
            else:
                try:
                    n = int(args[1]) - 1
                    page = help_pages[n]
                    assert(n >= 0)
                except AssertionError:
                    print(f"Cannot find help page {n+1}!")
                except IndexError:
                    print(f"Cannot find help page {n+1}!")
                except ValueError:
                    print(f"Cannot parse {args[1]} as an integer or "+
                          "command name!")
                else:
                    print(f"--Help page {n+1}--")
                    for command in page:
                        print("\n",command)
                        print(cmds_list[command])
        case "list":
            print("Available commands (aliases in <angle brackets>):")
            for command in sorted(cmds_list.keys()):
                if command in aliases:
                    print(f"<{command}>")
                else:
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
                polycount = len(polynomial.poly_dict.keys())
                print(f"Storing {polycount} polynomials:")
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
        case "deleteall" | "flush":
            if argc == 0 or args[1] != "CONFIRM":
                print("Confirm deletion of all stored polynomials "+
                      f"by typing `{cmd} CONFIRM`.")
            else:
                polynomial.poly_dict.clear()
                print("All stored polynomials deleted.")
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
        case "subtract" | "sub":
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
        case "lincomb" | "lc":
            if argc < 3:
                print("Too few arguments!")
                print(cmds_list[cmd])
                continue
            resultname = args[-1]
            if resultname in polynomial.poly_dict.keys():
                print(f"Cannot store linear combination in {result} -- "+
                      "name already in use.")
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
                    result = polynomial.lincomb(weights, polys)
                    polynomial.make_poly(resultname, result.coeffs)
                    print(f"Linear combination stored in {resultname}.")
        case "multiply" | "mul":
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
        case "power" | "pow":
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
                print(f"Euclidean division of {args[1]} by {args[2]} "+
                      "completed. Quotient and remainder stored in "+
                      f"{args[3]} and {args[4]} respectively.")
        case "eval":
            if argc < 2:
                print("Too few arguments!")
                print(cmds_list[cmd])
                continue
            try:
                poly = polynomial.poly_dict[args[1]]
                result = poly.peval(int(args[2]))
            except KeyError as e:
                name = e.args[0]
                print(f"Polynomial {name} not found!")
            except ValueError:
                print(f"Could not parse {args[2]} as integer!")
            else:
                print(f"{name}({args[2]}) = {result}")
        case "modulo" | "mod":
            if argc < 3:
                print("Too few arguments!")
                print(cmds_list[cmd])
                continue
            try:
                parith.modmake_poly(args[1], args[2], args[3])
            except (ZeroDivisionError, ArithmeticError, ValueError) as e:
                print(e)
            except KeyError as e:
                name = e.args[0]
                print(f"Polynomial {name} not found!")
            else:
                print(f"Remainder of {args[1]} mod {args[2]} "+
                      f"stored in {args[3]}.")
        case "eea":
            if argc < 5:
                print("Too few arguments!")
                print(cmds_list[cmd])
                continue
            try:
                parith.eea_make_poly(args[1],args[2],args[3],args[4],args[5])
            except KeyError as e:
                name = e.args[0]
                print(f"Polynomial {name} not found!")
            except ValueError as e:
                print(e)
            else:
                print("Extended Euclidean algorithm performed on "+
                      f"polynomials {args[1]} and {args[2]}. "+
                      f"GCD stored in {args[3]}, coefficients "+
                      f"stored in {args[4]} and {args[5]}.")
        case _:
            print(f"Unknown command: {cmd}!")
