# main program
# contains interface logic

# auxiliary stuff
import auxiliaries as aux
# help messages offloaded here to prevent bloat
import cmdinfo

import polynomial as pol
import parith
import pprops

exitflag = False

# warning flag for setchar
charflag = False

welcomemsg = ("Welcome to Finite Field Polynomial Calculator!\n\n"+
              f"Default field characteristic is {pol.FCH}.\n"+
              "To set the characteristic, use the `setchar` command.\n\n"+
              "Current display options are:\n"+
              str(pol.display_cfg)+"\n\n"+
              "Type `list` for all available commands, "+
              "or `help` (without back-quotes) for general info.")
print(welcomemsg)


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
                print(cmdinfo.cmds_list[cmd])
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
                        pol.set_characteristic(new_char)
                    except ValueError as e:
                        print(e)
                    else:
                        print(f"Characteristic set to {new_char} successfully.")
                        charflag = False
                        
        case "char":
            print(f"Field characteristic is {pol.FCH}.")
            
        case "exit" | "quit":
            print("Goodbye.")
            exitflag = True
            
        case "help":
            # if user typed only "help", return special help msg
            if argc == 0:
                print(cmdinfo.special_help_msg)
            elif args[1] in cmdinfo.cmds_list.keys():
                print(cmdinfo.cmds_list[args[1]])
            else:
                try:
                    n = int(args[1]) - 1
                    page = cmdinfo.help_pages[n]
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
                        print(cmdinfo.cmds_list[command])
                        
        case "list":
            print("Available commands (aliases in <angle brackets>):")
            for command in sorted(cmdinfo.cmds_list.keys()):
                if command in cmdinfo.aliases:
                    print(f"<{command}>")
                else:
                    print(command)
                    
        case "displayopts" | "dpo":
            # no args => print all current options
            if argc == 0:
                opts = str(pol.display_cfg)
                print(f"Current display options:\n{opts}")
            elif args[1] not in pol.opttags.keys():
                print(f"Unrecognized display option '{args[1]}'!")
            elif argc >= 1:
                option = args[1]
                optionname = pol.singleopts_names[option][0]
                # no 2nd argument => report option
                if argc == 1:
                    if pol.opttags[option] in pol.display_cfg:
                        optionstate = pol.singleopts_names[option][2]
                    else:
                        optionstate = pol.singleopts_names[option][1]
                    print(f"{optionname} is currently: {optionstate}")
                elif argc >= 2 and args[2] == "toggle":
                    # toggle option
                    pol.display_cfg = pol.display_cfg ^ pol.opttags[option]
                    # a bit WET, but i don't know how to do it better
                    if pol.opttags[option] in pol.display_cfg:
                        optionstate = pol.singleopts_names[option][2]
                    else:
                        optionstate = pol.singleopts_names[option][1]
                    print(f"{optionname} has been set to: {optionstate}")
                else:
                    # user has entered a valid display option, but
                    # 2nd argument is not "toggle"
                    print("Second argument must be `toggle` or absent.")
                    print(cmdinfo.cmds_list["displayopts"])
                    
        # data management commands        
        case "create":
            if argc == 0:
                print("Too few arguments!")
                print(cmdinfo.cmds_list[cmd])
                continue
            try:
                pol.make_poly(name, args[2:])
            except ValueError as e:
                print(e)
            else:
                print(f"Polynomial {name} created.")

        case "createbinary" | "cbin":
            if argc == 0:
                print("Too few arguments!")
                print(cmdinfo.cmds_list["createbinary"])
                continue
            if pol.FCH != 2:
                print("This command is only available in "+
                      "characteristic 2.")
                continue
            degs = []
            # parse degrees list
            try:
                for arg in args[2:]:
                    d = int(arg)
                    assert(d >= 0)
                    degs.append(d)
            except ValueError:
                print(f"Cannot parse {arg} as integer!")
            except AssertionError:
                print(f"Cannot include negative exponent {d}!")
            # construct coeffs
            coeffs = [0] * (max(degs) + 1)
            for d in degs:
                coeffs[d] += 1
            try:
                pol.make_poly(args[1], coeffs)
            except ValueError as e:
                print(e)
            else:
                print(f"Polynomial {args[1]} created.")
                
        case "show":
            if argc == 0:
                print(cmdinfo.cmds_list[cmd])
                continue
            try:
                display_string = pol.display_poly(name)
            except KeyError as e:
                name = e.args[0]
                print(f"No polynomial by name {name} to print.")
            else:
                print(display_string)
                
        case "showall":
            if len(pol.poly_dict.keys()) == 0:
                print("No polynomials currently stored.")
            else:
                polycount = len(pol.poly_dict.keys())
                plural_suffix = "s"
                if polycount == 1:
                    plural_suffix = ""
                print(f"Storing {polycount} polynomial{plural_suffix}:")
                print(pol.display_all())
                
        case "delete" | "del":
            if argc == 0:
                print("Too few arguments!")
                print(cmdinfo.cmds_list[cmd])
                continue
            delnames = args[1:]
            deletion_count = 0
            # go through the list of names
            # delete what we can
            # and what we can't, tell the user as such
            # and keep going
            for name in delnames:
                try:
                    pol.del_poly(name)
                except KeyError as e:
                    badname = e.args[0]
                    print(f"No polynomial by name {badname} to delete!")
                else:
                    deletion_count += 1
                    print(f"Polynomial {name} deleted.")
            # report how many polynomials got deleted
            plural_suffix = "s"
            if deletion_count == 1:
                plural_suffix = ""
            print(f"{deletion_count} polynomial{plural_suffix} "+
                  "deleted.")
                
        case "deleteall" | "flush":
            if argc == 0 or args[1] != "CONFIRM":
                print("Confirm deletion of all stored polynomials "+
                      f"by typing `{cmd} CONFIRM`.")
            else:
                pol.poly_dict.clear()
                print("All stored polynomials deleted.")
                
        case "update":
            if argc == 0:
                print(cmdinfo.cmds_list[cmd])
                continue
            try:
                pol.update_poly(name, args[2:])
            except KeyError as e:
                name = e.args[0]
                print(f"No polynomial by name {name} to update! "+
                      "Use `create` to create new polynomials.")
            else:
                print(f"Polynomial {name} updated.")
                
        case "copy":
            if argc < 2:
                print("Too few arguments!")
                print(cmdinfo.cmds_list[cmd])
                continue
            try:
                pol.copy_poly(args[1], args[2])
            except KeyError as e:
                name = e.args[0]
                print(f"No polynomial by name {name} to copy.")
            else:
                print(f"Polynomial {args[1]} copied to {args[2]}.")
                
        case "rename":
            if argc < 2:
                print("Too few arguments!")
                print(cmdinfo.cmds_list[cmd])
                continue
            try:
                pol.rename_poly(args[1], args[2])
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
                print(cmdinfo.cmds_list[cmd])
                continue
            # user supplied only 2 addends
            if argc == 3:
                try:
                    parith.addmake_poly(args[1], args[2], args[3])
                except ValueError as e:
                    print(e)
                except KeyError as e:
                    name = e.args[0]
                    print(f"Polynomial {name} not found!")
                else:
                    print(f"Sum {args[1]} + {args[2]} stored in {args[3]}.")
            # user supplied 3+ addends -- call new list-addition function
            else:
                addendnames = args[1:-1]
                resultname = args[-1]
                try:
                    parith.listaddmake_poly(addendnames, resultname)
                except ValueError as e:
                    print(e)
                except KeyError as e:
                    name = e.args[0]
                    print(f"Polynomial {name} not found!")
                else:
                    sumstr = " + ".join(addendnames)
                    print(f"Sum {sumstr} stored in {resultname}.")
                
        case "subtract" | "sub":
            if argc < 3:
                print("Too few arguments!")
                print(cmdinfo.cmds_list[cmd])
                continue
            try:
                parith.submake_poly(args[1], args[2], args[3])
            except ValueError as e:
                print(e)
            except KeyError as e:
                name = e.args[0]
                print(f"Polynomial {name} not found!")
            else:
                print(f"Difference {args[1]} - {args[2]} stored in {args[3]}.")
                
        case "lincomb" | "lc":
            if argc < 3:
                print("Too few arguments!")
                print(cmdinfo.cmds_list[cmd])
                continue
            resultname = args[-1]
            if resultname in pol.poly_dict.keys():
                print(f"Cannot store linear combination in {result} -- "+
                      "name already in use.")
            else:
                try:
                    weights, polynames = aux.parse_lincomb(args[1:-1])
                except ValueError as e:
                    print(e)
                except KeyError as e:
                    name = e.args[0]
                    print(f"Polynomial {name} not found!")
                else:
                    polys = []
                    for i in range(len(polynames)):
                        polys.append(pol.poly_dict[polynames[i]])
                    result = pol.lincomb(weights, polys)
                    pol.make_poly(resultname, result.coeffs)
                    print(f"Linear combination stored in {resultname}.")
                    
        case "multiply" | "mul":
            if argc < 3:
                print("Too few arguments!")
                print(cmdinfo.cmds_list[cmd])
                continue
            # user supplied only 2 factors
            if argc == 3:
                try:
                    parith.mulmake_poly(args[1], args[2], args[3])
                except ValueError as e:
                    print(e)
                except KeyError as e:
                    name = e.args[0]
                    print(f"Polynomial {name} not found!")
                else:
                    print(f"Product {args[1]} * {args[2]} stored in {args[3]}.")
            else:
                factornames = args[1:-1]
                resultname = args[-1]
                try:
                    parith.listmulmake_poly(factornames, resultname)
                except ValueError as e:
                    print(e)
                except KeyError as e:
                    name = e.args[0]
                    print(f"Polynomial {name} not found!")
                else:
                    prodstr = " * ".join(factornames)
                    print(f"Product {prodstr} stored in {resultname}.")
                
        case "power" | "pow":
            if argc < 3:
                print("Too few arguments!")
                print(cmdinfo.cmds_list[cmd])
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
                print(cmdinfo.cmds_list[cmd])
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
                print(cmdinfo.cmds_list[cmd])
                continue
            try:
                poly = pol.poly_dict[args[1]]
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
                print(cmdinfo.cmds_list[cmd])
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
                print(cmdinfo.cmds_list[cmd])
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
                      f"polynomials {args[1]} and {args[2]}.\n"+
                      f"GCD stored in {args[3]}, Bezout coefficients "+
                      f"stored in {args[4]} and {args[5]}.")
                
        case "diff":
            if argc < 2:
                print("Too few arguments!")
                print(cmdinfo.cmds_list[cmd])
            order = 1
            if argc >= 3:
                try:
                    order = int(args[3])
                except ValueError as e:
                    print(f"Could not parse {args[3]} as integer!")
            try:
                parith.diffmake_poly(args[1], order, args[2])
            except KeyError as e:
                name = e.args[0]
                print(f"Polynomial {name} not found!")
            except ValueError as e:
                print(e)
            else:
                print(f"{order}{aux.ordinal_suffix(order)} derivative "+
                      f"of {args[1]} stored in {args[2]}.")
        # property commands
        case "degree" | "deg":
            if argc == 0:
                print("Too few arguments!")
                print(cmdinfo.cmds_list["degree"])
                continue
            try:
                poly = pol.poly_dict[args[1]]
                result = poly.degree()
            except KeyError as e:
                name = e.args[0]
                print(f"Polynomial {name} not found!")
            else:
                print(f"deg({args[1]}) = {result}")
                
        case "irred":
            if argc == 0:
                print("Too few arguments!")
                print(cmdinfo.cmds_list[cmd])
                continue
            if argc >= 2 and args[2] != "reason":
                print("Second argument must be `reason` or absent.")
                print(cmdinfo.cmds_list[cmd])
                continue
            try:
                poly = pol.poly_dict[args[1]]
            except KeyError as e:
                name = e.args[0]
                print(f"Polynomial {name} not found!")
            else:
                irred_result = pprops.is_irreducible(poly)
                if argc == 1:
                    print(f"Polynomial {args[1]} is "+
                          irred_result.verdict_stmt()+".")
                # if we're here, `reason` option has been supplied.
                else:
                    print(f"Polynomial {args[1]} is {str(irred_result)}.")
                
        case "prim":
            if argc == 0:
                print("Too few arguments!")
                print(cmdinfo.cmds_list[cmd])
                continue
            try:
                poly = pol.poly_dict[args[1]]
            except KeyError as e:
                name = e.args[0]
                print(f"Polynomial {name} not found!")
            else:
                if pprops.is_primitive(poly):
                    verdict = "primitive"
                else:
                    verdict = "NOT primitive"
                print(f"Polynomial {args[1]} is {verdict}.")
        case _:
            print(f"Unknown command: {cmd}!")
