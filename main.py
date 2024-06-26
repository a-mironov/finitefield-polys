# main program
# contains interface logic

# auxiliary stuff
from math import gcd
import auxiliaries as aux
# help messages offloaded here to prevent bloat
import cmdinfo

import polynomial as pol
import pprops
import nonprimefield as npf

# all data management lives here
import datamgmt as dm
import fileio

exitflag = False

# warning flag for setchar
charflag = False

welcomemsg = ("Welcome to Finite Field Polynomial Calculator!\n\n"+
              f"Default field characteristic is {pol.FCH}.\n"+
              "To set the characteristic, use the `setchar` command.\n\n"+
              "Current display options are:\n"+
              str(pol.display_cfg)+"\n\n"+
              "Type 'list' for all available commands.\n"+
              "Type 'help' for general info.")
print(welcomemsg)

# for echoing creation/deletion/etc.
typenames = {"poly": "Polynomial", "el": "Field element"}

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

    # implementing "cp" and "ce" shortcuts
    if cmd == "cp" or cmd == "ce":
        args[0] = "create"
        match cmd:
            case "cp":
                args.insert(1,"poly")
            case "ce":
                args.insert(1,"el")
        cmd = "create"

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
            # easter egg
            if int(args[1]) == 57:
                print("Nice try, Grothendieck.")
                continue
            if not charflag:
                print("Warning! Changing the characteristic will "
                      "delete all stored polynomials! Repeat "
                      "the command to confirm.")
                charflag = True
                continue
            else:
                try:
                    new_char = int(args[1])
                except ValueError:
                    print(f"Could not parse {args[1]} as an integer!")
                else:
                    try:
                        dm.set_characteristic(new_char)
                    except ValueError as e:
                        print(e)
                    else:
                        print("Characteristic set to "
                              f"{new_char} successfully.")
                        # char changed => flush old quotpoly
                        charflag = False
                        
        case "char":
            print(f"Field characteristic is {pol.FCH}.")

        case "setfield":
            if argc == 0:
                print("Too few arguments!")
                print(cmdinfo.cmds_list[cmd])
                continue
            if args[1] not in dm.obj_dict.keys():
                print(f"Polynomial {args[1]} not found!")
                continue
            if ((argc == 1 or args[2] != "CONFIRM")
                and npf.FieldEl.quotpoly is not None):
                print("Warning! Changing the quotient polynomial will "
                      "delete all stored elements! Type "
                      f"`setfield {args[1]} CONFIRM` to confirm "
                      "field re-initialization.")
                continue
            dm.set_field(args[1])

        case "field":
            if npf.FieldEl.quotpoly is None:
                print("Non-prime field not yet initialized.")
            print("Current non-prime field is:\n"
                  f"GF({pol.FCH}^{npf.FieldEl.quotpoly.degree()})\n"
                  "represented as "
                  f"F_{pol.FCH}[x]/({str(npf.FieldEl.quotpoly)})")
            
        case "exit" | "quit":
            print("Goodbye.")
            exitflag = True
            
        case "help":
            # if user typed only "help", return special help msg
            if argc == 0:
                print(cmdinfo.special_help_msg)
            # command-specific help desc
            elif args[1] in cmdinfo.cmds_list.keys():
                print(cmdinfo.cmds_list[args[1]])
            # help page
            else:
                try:
                    n = int(args[1]) - 1
                    page = cmdinfo.help_pages[n]
                    assert(n >= 0)
                except (AssertionError, IndexError):
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
            print()
                    
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
                    
        # internal data management commands        
        case "create":
            if argc < 2:
                print("Too few arguments!")
                print(cmdinfo.helpdesc(cmd))
                continue
            if args[1] == "el" and npf.FieldEl.quotpoly is None:
                print("Cannot create field elements -- No field "
                      "initialized.")
                continue
            try:
                dm.make(args[2], args[3:], mode = args[1])
            except ValueError as e:
                print(e)
            else:
                typedesc = typenames[args[1]]
                print(f"{typedesc} {args[2]} created.")

        case "createbinary" | "cbin":
            if argc < 2:
                print("Too few arguments!")
                print(cmdinfo.helpdesc(cmd))
                continue
            if pol.FCH != 2:
                print("This command is only available in "+
                      "characteristic 2.")
                continue
            degs = []
            # parse degrees list
            try:
                for arg in args[3:]:
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
                dm.make(args[2], coeffs, mode = args[1])
            except ValueError as e:
                print(e)
            else:
                typedesc = typenames[args[1]]
                print(f"{typedesc} {args[2]} created.")
                
        case "show":
            if argc == 0:
                print(cmdinfo.helpdesc(cmd))
                continue
            try:
                display_string = dm.display(args[1])
            except KeyError as e:
                name = e.args[0]
                print(f"No polynomial by name {name} to print.")
            else:
                print(display_string)
                
        case "showall":
            if len(dm.obj_dict.keys()) == 0:
                print("Nothing currently stored.")
                continue
            polycount = len(dm.get_names_by_type("poly"))
            elcount = len(dm.get_names_by_type("el"))
            if argc == 0:
                # show everything
                print(f"Storing {aux.numphrase('polynomial',polycount)}, "
                      f"and {aux.numphrase('field element',elcount)}\n"
                      f"in field "
                      f"F_{pol.FCH}[x]/({str(npf.FieldEl.quotpoly)}):\n")
                print(dm.display_all())
            else:
                if args[1] == "poly":
                    print("Storing "+
                          aux.numphrase('polynomial',polycount)+":\n")
                if args[1] == "el":
                    print("Storing "+
                          aux.numphrase('field element',elcount)+
                          " in field "
                          f"GF({pol.FCH}^{npf.FieldEl.quotpoly.degree()})"
                          f" = F_{pol.FCH}[x]"
                          f"/({str(npf.FieldEl.quotpoly)}):\n")
                try:
                    print(dm.display_all(mode = args[1]),end="\n\n")
                except ValueError as e:
                    print(e)
                
        case "delete" | "del":
            if argc == 0:
                print("Too few arguments!")
                print(cmdinfo.helpdesc(cmd))
                continue
            delnames = args[1:]
            deletion_count = 0
            # go through the list of names
            # delete what we can
            # and what we can't, tell the user as such
            # and keep going
            for name in delnames:
                try:
                    typedesc = dm.get_type(name)
                    dm.delete(name)
                except KeyError as e:
                    badname = e.args[0]
                    print(f"No polynomial or field element "
                          f"by name {badname} to delete!")
                else:
                    deletion_count += 1
                    print(f"{typedesc} {name} deleted.")
            # report how many objects got deleted
            print(aux.numphrase("object",deletion_count)+
                  " deleted.")
                
        case "deleteall" | "flush":
            if argc == 1 and args[1] == "CONFIRM":
                dm.mass_delete("all")
                print("All stored objects deleted.")
                continue
            if argc < 2 or args[2] != "CONFIRM":
                print("Confirm deletion of all stored objects "+
                      f"by typing `{cmd} CONFIRM`.")
            else:
                match args[1]:
                    case "el":
                        dm.mass_delete("el")
                        print("All stored field elements deleted.")
                    case "poly":
                        dm.mass_delete("poly")
                        print("All stored polynomials deleted.")
                
        case "update":
            if argc == 0:
                print(cmdinfo.helpdesc(cmd))
                continue
            try:
                dm.update(args[1], args[2:])
            except KeyError as e:
                name = e.args[0]
                print("No polynomial or field element "
                      f"by name {name} to update! "+
                      "Use `create` to create new objects.")
            else:
                typedesc = dm.get_type(args[1])
                print(f"{typedesc} {args[1]} updated.")

        case "copy":
            if argc < 2:
                print("Too few arguments!")
                print(cmdinfo.helpdesc(cmd))
                continue
            try:
                dm.copy(args[1], args[2])
            except KeyError as e:
                name = e.args[0]
                print(f"No polynomial or field element "
                      "by name {name} to copy.")
            else:
                typedesc = dm.get_type(args[1])
                print(f"{typedesc} {args[1]} copied to {args[2]}.")
                
        case "rename":
            if argc < 2:
                print("Too few arguments!")
                print(cmdinfo.helpdesc(cmd))
                continue
            try:
                dm.rename(args[1], args[2])
            except KeyError as e:
                name = e.args[0]
                print(f"No polynomial by name {name} to rename.")
            except ValueError as e:
                print(e)
            else:
                typedesc = dm.get_type(args[2])
                print(f"{typedesc} {args[1]} renamed to {args[2]}.")

        # file IO commands
        case "save":
            if argc < 1:
                print("Too few arguments!")
                print(cmdinfo.cmds_list[cmd])
                continue
            filename = args[1]
            try:
                fileio.save_workspace(filename)
            except IOError as e:
                print(f"Could not save workspace: {e}")
            else:
                print(f"Workspace saved to file \\saves\\{filename}"
                       " successfully.")
        
        case "load":
            if argc < 1:
                print("Too few arguments!")
                print(cmdinfo.cmds_list[cmd])
                continue
            filename = args[1]
            try:
                fileio.load_workspace(filename)
            except (IOError, ValueError) as e:
                print(e)
            else:
                print(f"Workspace loaded from file \\saves\\{filename}"
                       " successfully.")

        # arithmetic commands        
        case "add":
            if argc < 3:
                print("Too few arguments!")
                print(cmdinfo.helpdesc(cmd))
                continue
            addendnames = args[1:-1]
            resultname = args[-1]

            try:
                dm.addmake(addendnames, resultname)
            except (ValueError, AttributeError) as e:
                print(e)
            except KeyError as e:
                name = e.args[0]
                print(f"Object {name} not found!")
            else:
                sumstr = " + ".join(addendnames)
                print(f"Sum {sumstr} stored in {resultname}.")
                
        case "subtract" | "sub":
            if argc < 3:
                print("Too few arguments!")
                print(cmdinfo.helpdesc(cmd))
                continue
            try:
                dm.submake(args[1:3], args[3])
            except (ValueError, AttributeError) as e:
                print(e)
            except KeyError as e:
                name = e.args[0]
                print(f"Object {name} not found!")
            else:
                print(f"Difference {args[1]} - {args[2]} stored in {args[3]}.")

        # TBD. maybe only for polys?
        case "lincomb" | "lc":
            if argc < 3:
                print("Too few arguments!")
                print(cmdinfo.helpdesc(cmd))
                continue
            resultname = args[-1]
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
                    polys.append(dm.obj_dict[polynames[i]])
                try:
                    result = pol.lincomb(weights, polys)
                except AttributeError:
                    print("Linear combinations implemented for "
                          "polynomials only.")
                except KeyError as e:
                    name = e.args[0]
                    print(f"Polynomial {name} not found!")
                else:
                    dm.make(resultname, result.coeffs, mode="poly")
                    print(f"Linear combination stored in {resultname}.")
                    
        case "multiply" | "mul":
            if argc < 3:
                print("Too few arguments!")
                print(cmdinfo.helpdesc(cmd))

            addendnames = args[1:-1]
            resultname = args[-1]

            try:
                dm.mulmake(addendnames, resultname)
            except (ValueError, AttributeError) as e:
                print(e)
            except KeyError as e:
                name = e.args[0]
                print(f"Object {name} not found!")
            else:
                prodstr = " * ".join(addendnames)
                print(f"Product {prodstr} stored in {resultname}.")

        case "divide" | "div":
            if argc < 3:
                print("Too few arguments!")
                print(cmdinfo.helpdesc(cmd))
                continue
            try:
                dm.divmake_el(args[1:3], args[3])
            except (ValueError, AttributeError) as e:
                print(e)
            except KeyError as e:
                name = e.args[0]
                print(f"Object {name} not found!")
            else:
                print(f"Quotient {args[1]} / {args[2]} "
                      f"stored in {args[3]}.")
                
        case "power" | "pow":
            if argc < 3:
                print("Too few arguments!")
                print(cmdinfo.helpdesc(cmd))
                continue
            try:
                dm.powmake(args[1], int(args[2]), args[3])
            except ValueError as e:
                print(e)
            except KeyError as e:
                name = e.args[0]
                print(f"Object {name} not found!")
            else:
                print(f"Power {args[1]}^{args[2]} stored in {args[3]}.")
                
        case "eucdiv":
            if argc < 4:
                print("Too few arguments!")
                print(cmdinfo.helpdesc(cmd))
                continue
            try:
                dm.eucdivmake_poly(args[1], args[2], args[3], args[4])
            except TypeError:
                print(f"Input arguments {args[1]} and {args[2]} "
                      "must be polynomials!")
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
                print(cmdinfo.helpdesc(cmd))
                continue
            try:
                poly = dm.obj_dict[args[1]]
                result = poly.peval(int(args[2]))
            except KeyError as e:
                name = e.args[0]
                print(f"Polynomial {name} not found!")
            except ValueError:
                print(f"Could not parse {args[2]} as integer!")
            except AttributeError:
                print(f"Cannot evaluate field elements at points!")
            else:
                print(f"{args[1]}({args[2]}) = {result}")
                
        case "modulo" | "mod":
            if argc < 3:
                print("Too few arguments!")
                print(cmdinfo.helpdesc(cmd))
                continue
            try:
                dm.modmake_poly(args[1], args[2], args[3])
            except (ZeroDivisionError, ArithmeticError,
                    ValueError, TypeError) as e:
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
                print(cmdinfo.helpdesc(cmd))
                continue
            try:
                dm.eea_make_poly(args[1],args[2],args[3],args[4],args[5])
            except TypeError:
                print(f"Input arguments {args[1]} and {args[2]} "
                      "must be polynomials!")
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
                print(cmdinfo.helpdesc(cmd))
            order = 1
            if argc >= 3:
                try:
                    order = int(args[3])
                except ValueError as e:
                    print(f"Could not parse {args[3]} as integer!")
            try:
                dm.diffmake_poly(args[1], order, args[2])
            except AttributeError:
                print(f"Input arguments {args[1]} and {args[2]} "
                      "must be polynomials!")
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
                print(cmdinfo.helpdesc(cmd))
                continue
            try:
                poly = dm.obj_dict[args[1]]
                result = poly.degree()
            except AttributeError:
                print(f"Cannot print degree of {args[1]} -- Not a "
                      "polynomial.")
            except KeyError as e:
                name = e.args[0]
                print(f"Polynomial {name} not found!")
            else:
                print(f"deg({args[1]}) = {result}")

        case "dlog":
            if argc == 0:
                print("Too few arguments!")
                print(cmdinfo.helpdesc(cmd))
                continue
            name = args[1]
            if name not in dm.obj_dict.keys():
                print(f"Field element {name} not found!")
            elif type(dm.obj_dict[name]) == pol.Poly:
                print("Cannot take discrete logarithm of "
                      f"polynomial {name}!")
            else:
                el = dm.obj_dict[name]
                if el == npf.FieldEl(0):
                    print(f"{name} is 0 and does not have "
                          "a discrete logarithm.")
                else:
                    print(f"log_a({str(el)}) = {el.dlog}")
        case "coeff":
            if argc < 2:
                print("Too few arguments! No help desc yet.")
                continue
            try:
                poly = dm.obj_dict[args[1]]
                pow = int(args[2])
                assert pow > 0
            except AssertionError:
                print(f"Cannot query coefficients of negative powers!")
                continue
            except ValueError:
                print(f"Could not parse {args[2]} as integer!")
                continue
            except KeyError:
                print(f"Polynomial {args[1]} not found!")
                continue
            varletter = "x"
            if type(poly) is npf.FieldEl:
                poly = poly.poly 
                varletter = "a"
                assert type(poly) is pol.Poly
            coeff = 0
            if pow > poly.degree():
                coeff = 0
            else:
                coeff = poly.coeffs[pow]
            if (pol.DisplayFlag.BALANCED in pol.display_cfg
                and pol.FCH != 2
                and coeff > (pol.FCH - 1)//2):
                coeff -= pol.FCH
            print(f"Coefficient of {varletter}^{pow} in {args[1]} is {coeff}.")
        case "order":
            if argc == 0:
                print("Too few arguments!")
                print(cmdinfo.helpdesc(cmd))
                continue
            name = args[1]
            if name not in dm.obj_dict.keys():
                print(f"Field element {name} not found!")
            elif type(dm.obj_dict[name]) == pol.Poly:
                print("Cannot take order of "
                      f"polynomial {name}!")
            else:
                el = dm.obj_dict[name]
                if el == npf.FieldEl(0):
                    print(f"{name} is 0 and does not belong "
                          "to the multiplicative group.")
                else:
                    grpsize = (pol.FCH
                               ** npf.FieldEl.quotpoly.degree()
                               - 1)
                    divisor = gcd(grpsize, el.dlog)
                    el_order = grpsize // divisor
                    print(f"ord({name}) = {el_order}")
                    if divisor == 1:
                        print(f"{name} is primitive!")
        case "irred":
            if argc == 0:
                print("Too few arguments!")
                print(cmdinfo.helpdesc(cmd))
                continue
            if argc >= 2 and args[2] != "reason":
                print("Second argument must be `reason` or absent.")
                print(cmdinfo.helpdesc(cmd))
                continue
            try:
                poly = dm.obj_dict[args[1]]
            except KeyError as e:
                name = e.args[0]
                print(f"Polynomial {name} not found!")
            else:
                try:
                    irred_result = pprops.is_irreducible(poly)
                except AttributeError:
                    print(f"Cannot check {args[1]} for irreducibility -- "
                          "Not a polynomial.")
                if argc == 1:
                    print(f"Polynomial {args[1]} is "+
                          irred_result.verdict_stmt()+".")
                # if we're here, `reason` option has been supplied.
                else:
                    print(f"Polynomial {args[1]} is {str(irred_result)}.")
                
        case "prim":
            if argc == 0:
                print("Too few arguments!")
                print(cmdinfo.helpdesc(cmd))
                continue
            try:
                poly = dm.obj_dict[args[1]]
            except KeyError as e:
                name = e.args[0]
                print(f"Polynomial {name} not found!")
            else:
                try:
                    if pprops.is_primitive(poly):
                        verdict = "primitive"
                    else:
                        verdict = "NOT primitive"
                    print(f"Polynomial {args[1]} is {verdict}.")
                except AttributeError:
                    print(f"Cannot check {args[1]} for primitivity -- "
                          "Not a polynomial.")
        case _:
            print(f"Unknown command: {cmd}!")
