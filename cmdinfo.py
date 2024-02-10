# cmdinfo module

# contains help messages for all currently supported commands
# moved here from `main.py` to relieve bloat
# and ease navigation

# contains the following objects, and no more:
# 1. cmds_list -- dict of commands and their help descriptions
# 2. aliases -- list of commands that alias other commands
# 3. help_pages -- list of lists to group commands into pages
#    for the purposes of `help <n>`
# 4. special_help_msg -- message to be printed 

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
cmds_list["displayopts"] = ("Usage: displayopts OR displayopts <option> OR "+
                            "displayopts <option> toggle\n\n"+
                            "With no input, displays all current display "+
                            "options.\nWith only <option> as input, "+
                            "displays the state of that option.\nWith "+
                            "`<option> toggle` as input, toggles that option "+
                            "and reports its new value.\n\n"+
                            "Currently available options:\n"+
                            "deg -- Term order (ascending or descending "+
                            "by degree)\n"+
                            "bal -- Coefficient display mode "+
                            "(balanced or unbalanced)\n"+
                            "\nN.B.:\n\n"+
                            "* `bal` option is IGNORED "+
                            "in characteristic 2.\n"+
                            "* `deg` option does NOT affect inputs for the "+
                            "`create` and `update` commands -- these always "+
                            "read coefficients in ascending order."
                            "\n\nAlias: dpo")
cmds_list["dpo"] = ("Alias for `displayoptions`.")
aliases.append("dpo")
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
cmds_list["delete"] = ("Usage: delete <name1> [<name2> [...]]\n\n"+
                       "Deletes all polynomials under the "+
                       "specified names, of which "+
                       "there must be at least one.\n"+
                       "On names that don't exist, "+
                       "prints an alert to that effect.\n"+
                       "Deletes all specified names that were found.\n\n"
                       "Alias: del")
cmds_list["del"] = ("Alias for `delete`.")
aliases.append("del")
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
cmds_list["add"] = ("Usage: add <name1> <name2> [<name3> ...] <result>\n\n"+
                    "Adds polynomials under all supplied names "+
                    "(except `result`) and stores the sum under "+
                    "name `result`.\n\n"+
                    "At least 3 arguments must be supplied; `result` "+
                    "is always the last, and must not exist.")
cmds_list["subtract"] = ("Usage: subtract <name1> <name2> <result>\n\n"+
                    "Subtracts the polynomials by names `name1` and `name2` "+
                    "and stores the result in `result`. `name1` and `name2` "+
                    "must exist, while `result` must not exist.\n\n"+
                    "Alias: sub")
cmds_list["sub"] = ("Alias for `subtract`.")
aliases.append("sub")
cmds_list["multiply"] = ("Usage: "+
                         "multiply <name1> <name2> [<name3> ...] <result>\n\n"+
                         "Multiplies polynomials under all supplied names "+
                         "(except `result`) and stores the sum under "+
                         "name `result`.\n\n"+
                         "At least 3 arguments must be supplied; `result` "+
                         "is always the last, and must not exist"
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
cmds_list["diff"] = ("Usage: diff <name> <result> OR "+
                     "diff <name> <result> <order>\n\n"+
                     "Differentiates polynomial `name` `order` times "+
                     "and stores the result in `result` "+
                     "(which must not exist).\n"+
                     "With `order` not specified, differentiates once "+
                     "(i.e. takes the 1st derivative).")
# property commands
cmds_list["degree"] = ("Usage: degree <name>\n\n"+
                       "Prints the degree of the polynomial `name` on "+
                       "the screen.\n\n"+
                       "Alias: deg")
cmds_list["deg"] = ("Alias for `degree`.")
aliases.append("deg")
cmds_list["irred"] = ("Usage: irred <name> [reason]\n\n"+
                      "Checks if polynomial `name` is irreducible, "+
                      "and prints the result on the screen.\n"+
                      "If second argument is `reason`, also prints "+
                      "the reason for (ir)reducibility as detected "+
                      "by the irreducibility checker.")

help_pages = [["exit","help","list","setchar","char","displayopts"],
              ["create","show","showall","delete","update","copy","rename"],
              ["add","subtract","multiply","lincomb",
               "power","eval","modulo","eucdiv","eea","diff"],
              ["degree", "irred"]]

special_help_msg = ("Type `list` to see all commands.\n"+
                    "Type `help <cmd>` to view the description of one command,"+
                    "or type `help <n>` to view descriptions for all commands "+
                    "in one of the following groups:\n\n"+
                    "1. General commands\n"+
                    "2. Data management commands\n"+
                    "3. Arithmetic commands\n"+
                    "4. Property commands")
