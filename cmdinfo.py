# cmdinfo module

# contains help messages for all currently supported commands
# moved here from `main.py` to relieve bloat
# and ease navigation

# contains the following objects, and no more:
# 1. cmds_list -- dict of commands and their help descriptions
# 2. aliases -- dict of commands that alias other commands
# 3. help_pages -- list of lists to group commands into pages
#    for the purposes of `help <n>`
# 4. special_help_msg -- message to be printed on receipt of
#    the command `help` with no arguments
# 5. dealias -- helper function to dereference aliases

## command help messages
cmds_list = {}
aliases = {}
# general and initialization commands
cmds_list["exit"] = ("Usage: exit\n\n"+
                     "Exits the program.\n\n"+
                     "Alias: quit")
cmds_list["quit"] = ("Alias for `exit`.")
aliases["quit"] = "exit"
cmds_list["help"] = ("Usage: help OR help <cmd> OR help <n>\n\n"+
                     "With no input, prints the list of help pages.\n"+
                     "With a command, prints the description and usage "+
                     "for that command.\nWith a number, prints description "+
                     "and usage for all commands on that help page.")
cmds_list["list"] = ("Usage: list\n\n"+
                     "Lists all currently supported commands.")
cmds_list["setchar"] = ("Usage: setchar <number> [CONFIRM]\n\n"+
                        "Sets the base field characteristic to `number`. "+
                        "If this causes a change, all stored objects "+
                        "are deleted, and the non-prime field is reset! "
                        "Warns the user before proceeding.\n"+
                        "If second argument is present and equal to "+
                        "'CONFIRM', in all caps, without quotes, "+
                        "this command bypasses the warning.")
cmds_list["char"] = ("Usage: char\n\n"+
                     "Displays the current characteristic of the base field.")
cmds_list["setfield"] = ("Usage: setfield <name> [CONFIRM]\n\n"
                         "(Re)sets the polynomial used to define the "
                         "non-prime field GF(p^n) to do calculations in. "
                         "This command deletes all currently stored field "
                         "elements, but polynomials are kept intact."
                         "Requires confirmation in the form of 'CONFIRM' "
                         "(all caps, no quotes) as second argument, "
                         "unless the field is uninitialized.")                       
cmds_list["field"] = ("Usage: field\n\n"
                      "Displays the polynomial used to define the current "
                      "non-prime field GF(p^n).")
cmds_list["displayopts"] = ("Usage: displayopts OR displayopts <option> OR "
                            "displayopts <option> toggle\n\n"
                            "With no input, displays all current display "
                            "options.\nWith only <option> as input, "
                            "displays the state of that option.\nWith "
                            "`<option> toggle` as input, toggles that option "
                            "and reports its new value.\n\n"
                            "Currently available options:\n"
                            "bal -- Coefficient display mode "
                            "(balanced or unbalanced)\n"
                            "deg -- Term order (ascending or descending "
                            "by degree)\n"
                            "\nN.B.:\n\n"
                            "* `bal` option is IGNORED "
                            "in characteristic 2.\n"
                            "* `deg` option does NOT affect inputs for the "
                            "`create` and `update` commands -- these always "
                            "read coefficients in ascending order."
                            "\n\nAlias: dpo")
cmds_list["dpo"] = ("Alias for `displayoptions`.")
aliases["dpo"] = "displayoptions"

# data management commands
cmds_list["create"] = ("Usage: create <poly|el> <name> <coeffs>\n\n"
                       "Creates a polynomial or field element by name "
                       "`name` with coefficients `coeffs`, read in "
                       "ascending order of degree. The first argument "
                       "specifies the type to be created, and is "
                       "obligatory.\n\n"
                       "Aliases: `ce` for `create el`, "
                       "`cp` for `create poly`.")
cmds_list["ce"] = ("Alias for `create el`.")
cmds_list["cp"] = ("Alias for `create poly`.")
aliases["ce"] = "create"
aliases["cp"] = "create"
cmds_list["createbinary"] = ("Usage: createbinary <poly|el> <name> <degs>\n\n"
                             "Creates a polynomial or field element equal "
                             "to the sum of x^d for integers d in `degs`.\n"
                             "Works ONLY in characteristic 2.The first argument "
                             "specifies the type to be created, and is "
                             "obligatory.")
cmds_list["cbin"] = ("Alias for `createbinary`.")
aliases["cbin"] = "createbinary"
cmds_list["show"] = ("Usage: show <name>\n\n"
                     "Displays the polynomial or field element "
                     "by name `name` (if it exists) on the screen.")
cmds_list["showall"] = ("Usage: showall [poly|el]\n\n"
                        "If second argument is `poly` or `el`, displays all "
                        "currently stored polynomials or field elements "
                        "on the screen. If second argument is absent, "
                        "displays both.")
cmds_list["delete"] = ("Usage: delete <name1> [<name2> [...]]\n\n"
                       "Deletes all objects under the "
                       "specified names, of which "
                       "there must be at least one.\n"
                       "On names that don't exist, "
                       "prints an alert to that effect.\n"
                       "Deletes all specified names that were found.\n\n"
                       "Alias: del")
cmds_list["del"] = ("Alias for `delete`.")
aliases["del"] = "delete"
cmds_list["deleteall"] = ("Usage: deleteall [poly|el] CONFIRM\n\n"
                          "If the first argument is present as `poly` "
                          "or `el`, deletes all stored polynomials or field "
                          "elements respectively. If first argument is "
                          "absent, i.e. `deleteall CONFIRM`, deletes "
                          "everything. Does nothing without 'CONFIRM'."
                          "Alias: flush")
cmds_list["flush"] = ("Alias for `deleteall`.")
aliases["flush"] = "deleteall"
cmds_list["update"] = ("Usage: update <name> <coeffs>\n\n"
                       "Updates the polynomial or field element "
                       "by name `name` with new coefficients `coeffs`, "
                       "read in ascending order of degree.")
cmds_list["copy"] = ("Usage: copy <src> <dest>\n\n"
                     "Copies the object by name `src` into `dest`. Warning: "
                     "This command overwrites the object by name `dest` "
                     "if present!")
cmds_list["rename"] = ("Usage: rename <oldname> <newname>\n\n"
                       "Renames an object from `oldname` to `newname`.")
# arithmetic commands
cmds_list["add"] = ("Usage: add <name1> <name2> [<name3> ...] <result>\n\n"
                    "Adds polynomials or field elements under all supplied names "
                    "(except `result`) and stores the sum under "
                    "name `result`.\n\n"
                    "At least 3 arguments must be supplied; `result` "
                    "is always the last. Types cannot be mixed.")
cmds_list["subtract"] = ("Usage: subtract <name1> <name2> <result>\n\n"
                    "Subtracts the polynomials or field elements "
                    "by names `name1` and `name2` and stores the result "
                    "in `result`.n\n"
                    "Alias: sub")
cmds_list["sub"] = ("Alias for `subtract`.")
aliases["sub"] = "subtract"
cmds_list["multiply"] = ("Usage: "
                         "multiply <name1> <name2> [<name3> ...] <result>\n\n"
                         "Multiplies polynomials or field elements under "
                         "all supplied names (except `result`) and stores "
                         "the product under name `result`.\n\n"
                         "At least 3 arguments must be supplied; `result` "
                         "is always the last. Types cannot be mixed."
                         "Alias: mul")
cmds_list["mul"] = ("Alias for `multiply`.")
aliases["mul"] = "multiply"
cmds_list["lincomb"] = ("Usage: lincomb <weight1> <poly1> "
                        "[<weight2> <poly2> [...]] <result>\n\n"
                        "Computes a scalar linear combination of the "
                        "indicated polynomials and stores the result in "
                        "`result`.\n\n"
                        "Alias: lc")
cmds_list["divide"] = ("Usage: divide <name1> <name2> result\n\n"
                       "Divides two field elements by names `name1` and "
                       "`name2`, and stores the result in `result`.\n"
                       "Alias: div")
cmds_list["div"] = "Alias for `divide`."
aliases["div"] = "divide"
cmds_list["lc"] = ("Alias for `lincomb`.")
aliases["lc"] = "lincomb"
cmds_list["power"] = ("Usage: power <basename> <exponent> <result>\n\n"
                      "Raises the polynomial or field element "
                      "by name `basename` to power `exponent` and "
                      "stores the result in `result`.\n\n"
                      "Alias: pow")
cmds_list["pow"] = ("Alias for `power`.")
aliases["pow"] = "power"
cmds_list["eucdiv"] = ("Usage: eucdiv <dividend> <divisor> <quot> <rem>\n\n"
                       "Performs Euclidean division on polynomials "
                       "`dividend` and `divisor`, and stores the results "
                       "(quotient and remainder) under their indicated names.")
cmds_list["eval"] = ("Usage: eval <name> <point>\n\n"
                     "Evaluates the polynomial by name `name` at x = `point` "
                     "and prints the value on the screen.")
cmds_list["modulo"] = ("Usage: modulo <name> <modulus> <result>\n\n"
                       "Reduces polynomial `name` modulo polynomial "
                       "`modulus` and stores the result in `result` "
                       "(which must not exist).\n\n"
                       "Alias: mod")
cmds_list["mod"] = ("Alias for `modulo`.")
aliases["mod"] = "modulo"
cmds_list["eea"] = ("Usage: eea <poly1> <poly2> <gcd> <coe1> <coe2>\n\n"
                    "Performs the extended Euclidean algorithm on "
                    "polynomials `poly1` and `poly2`, finding their "
                    "greatest common divisor and its Bezout "
                    "coefficients. Stores the GCD under name `gcd`, "
                    "and the coefficients under names `coe1` and `coe2`. "
                    "All three output names must not exist.")
cmds_list["diff"] = ("Usage: diff <name> <result> OR "
                     "diff <name> <result> <order>\n\n"
                     "Differentiates polynomial `name` `order` times "
                     "and stores the result in `result` "
                     "(which must not exist).\n"
                     "With `order` not specified, differentiates once "
                     "(i.e. takes the 1st derivative).")
# property commands
cmds_list["degree"] = ("Usage: degree <name>\n\n"
                       "Prints the degree of the polynomial `name` on "
                       "the screen.\n\n"
                       "Alias: deg")
cmds_list["deg"] = ("Alias for `degree`.")
aliases["deg"] = "degree"
cmds_list["dlog"] = ("Usage: dlog <name>\n\n"
                     "Prints the discrete logarithm of field element "
                     "`name` on the screen.\nThe discrete logarithm "
                     "of a nonzero field element `e` of GF(p^n) "
                     "is the unique exponent k between 0 and p^n - 2 "
                     "such that a^k == e.")
cmds_list["order"] = ("Usage: order <name>\n\n"
                      "Prints the order of field element `name` in "
                      "the multiplicative group of GF(p^n).\nThe "
                      "order of an element `e` is the lowest "
                      "exponent n such that e^n = 1.")
cmds_list["irred"] = ("Usage: irred <name> [reason]\n\n"
                      "Checks if polynomial `name` is irreducible, "
                      "and prints the result on the screen.\n"
                      "If second argument is `reason`, also prints "
                      "the reason for (ir)reducibility as detected "
                      "by the irreducibility checker.")
cmds_list["prim"] = ("Usage: prim <name>\n\n"
                     "Checks if polynomial `name` is primitive.\n"
                     "Note: polynomials that are not irreducible, "
                     "as well as those of degree 1 or under, "
                     "are not considered primitive.")

help_pages = [["exit","help","list","setchar","char",
               "setfield","field","displayopts"],
              ["create","show","showall","delete",
               "deleteall","update","copy","rename"],
              ["add","subtract","multiply","divide","power",
               "lincomb","eval","modulo","eucdiv","eea","diff"],
              ["degree", "dlog", "order", "irred", "prim"]]

special_help_msg = ("Type `list` to see all commands.\n"
                    "Type `help <cmd>` to view the description of one command,"
                    "or type `help <n>` to view descriptions for all commands "
                    "in one of the following groups:\n\n"
                    "1. General commands\n"
                    "2. Data management commands\n"
                    "3. Arithmetic commands\n"
                    "4. Property commands")

def dealias(cmd: str):
    if cmd in aliases.keys():
        return aliases[cmd]
    elif cmd in cmds_list.keys():
        return cmd
    else:
        raise ValueError(f"Invalid command {cmd}!")

def helpdesc(cmd: str):
    return cmds_list[dealias(cmd)]