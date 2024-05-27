# fileio module
# contains logic for reading from & writing to files

import sys
import os
import datamgmt as dm
import polynomial as pol
import nonprimefield as npf

def raw_coeffs(obj):
    """
    Returns the raw coefficients of a Poly or FieldEl object,
    in ascending order and separated by spaces,
    e.g. x^2 + 3 -> "3 0 1".
    """
    if type(obj) is pol.Poly:
        return " ".join([str(coe) for coe in obj.coeffs])
    elif type(obj) is npf.FieldEl:
        return " ".join([str(coe) for coe in obj.poly.coeffs])
    else:
        raise TypeError(f"{obj} is not a polynomial or field element!")

# write to file
# extra argument for testing purposes
def save_workspace(filename: str):
    """
    Saves the current workspace to file `filename`.
    """
    # open the file
    s = open(os.getcwd() + "\\saves\\" + filename, mode="w")
    # save shit in the following order:
    # 1. "FFP" start line, which will be expected from reads
    s.write("FFP\n")
    # 2. field characteristic
    s.write(f"CHAR {pol.FCH}\n")
    # 3. if a quotient polynomial is present, write it down too
    if npf.FieldEl.quotpoly is not None:
        s.write(f"QUOT {raw_coeffs(npf.FieldEl.quotpoly)}\n")
    # 4. display options
    s.write("DISP ")
    s.write("term-desc" if pol.DisplayFlag.DESCENDING else "term-asc")
    s.write(" ")
    s.write("coeffs-bal" if pol.DisplayFlag.BALANCED else "coeffs-unbal")
    s.write("\n")
    # 5. polynomials and elements
    for name in dm.obj_dict:
        obj = dm.obj_dict[name]
        if type(obj) is pol.Poly:
            s.write("POLY ")
        if type(obj) is npf.FieldEl:
            s.write("EL ")
        s.write(name + " " + raw_coeffs(obj) + "\n")
    # close the file
    s.close()

def read_single_param(line: str, what_param: str, readflags: dict):
    # attempts to read a parameter from a TOKENIZED file line
    # called with tokens[1:]
    param_desc = {"CHAR":"characteristic",
                  "QUOT":"quotient polynomial",
                  "DISP":"display options"}
    param_lens = {"CHAR": 1, "DISP": 2}
    if readflags[what_param]:
        raise ValueError(f"Duplicate {param_desc[what_param]} specification")
    # reject quotient polynomials which have less than 3 coefficient (ie less than deg 2)
    # if user snuck in some 0 coefficients, let it be handled upstream
    if what_param == "QUOT":
        if len(line) < 3:
            raise ValueError(f"Missing quotient polynomial specification")
    else:
        if len(line) < param_lens[what_param]:
            raise ValueError(f"Short or empty {param_desc[what_param]} specification")
        if len(line) > param_lens[what_param]:
            raise ValueError(f"Overlong {param_desc[what_param]} specification")
    match what_param:
        case "CHAR":
            try:
                newchar = int(line[0])
            except ValueError:
                raise ValueError(f"Bad characteristic value -- "
                                 f"{line[0]}, cannot parse as integer")
            else:
                dm.set_characteristic(newchar)
        case "QUOT":
            try:
                coeffs = [int(coe) for coe in line]
            except ValueError:
                raise ValueError(f"Bad coefficient(s) for quotient polynomial")
            else:
                dm.make("_TMPQP",coeffs)
                dm.set_field("_TMPQP")
                dm.delete("_TMPQP")
        case "DISP":
            # should contain a term specification (term-asc or term-desc)
            # and a coefficient specification (coeffs-bal or coeffs-unbal)
            # in EITHER ORDER, which is the only reason im bothering
            # to make it this way
            # going to do it the bit-hacking way:
            # term-asc = 1, term-desc = 2, coeffs-bal = 4, coeffs-unbal = 8
            dispflags_found = 0
            dflags_values = {"term-asc":1, "term-desc":2,
                             "coeffs-bal":4, "coeffs-unbal":8}
            for word in dflags_values.keys():
                if word in line:
                    dispflags_found += dflags_values[word]
            # valid configurations are:
            # 1010 = 10 = unbal, desc
            # 1001 = 9 = unbal, asc
            # 0110 = 6 = bal, desc
            # 0101 = 5 = bal, asc
            match dispflags_found:
                case 5:
                    pol.display_cfg = pol.DisplayFlag.BALANCED
                case 6:
                    pol.display_cfg = pol.DisplayFlag.BALANCED | pol.DisplayFlag.DESCENDING
                case 9:
                    pol.display_cfg = ~(pol.DisplayFlag.BALANCED | pol.DisplayFlag.DESCENDING)
                case 10:
                    pol.display_cfg = pol.DisplayFlag.DESCENDING
                case _:
                    raise ValueError("Conflicting and/or incomplete display options")
    readflags[what_param] = True

def parse_disp(line):
    dispflags_found = 0
    dflags_values = {"term-asc":1, "term-desc":2,
                     "coeffs-bal":4, "coeffs-unbal":8}
    for word in dflags_values.keys():
        if word in line:
            dispflags_found += dflags_values[word]
    return dispflags_found

def validate_disp(line):
    return parse_disp(line) in [5,6,9,10]

def update_disp(dispflags):
    match dispflags:
        case 5:
            pol.display_cfg = pol.DisplayFlag.BALANCED
        case 6:
            pol.display_cfg = pol.DisplayFlag.BALANCED | pol.DisplayFlag.DESCENDING
        case 9:
            pol.display_cfg = ~(pol.DisplayFlag.BALANCED | pol.DisplayFlag.DESCENDING)
        case 10:
            pol.display_cfg = pol.DisplayFlag.DESCENDING
        case _:
            raise ValueError("Conflicting and/or incomplete display options")

def load_workspace(filename: str):
    # throws "too many values to unpack" error...
    """
    Loads a workspace from a file. Overwrites existing workspace.
    """
    filepath = os.getcwd() + "\\saves\\" + filename
    # throws error - will be handled upstream in main
    s = open(filepath, "r")
    # read things in the sameish order as save_workspace saves them
    # first line must be "FFP"
    # line = s.readline()[:-1] # to get rid of the newline
    # if line != "FFP":
    #     raise ValueError(f"File {filename} is not a recognized file -- "
    #                      f"first line expected \"FFP\", got \"{line}\".")
    # readflags = {"CHAR":False, "QUOT":False, "DISP":False}
    parsed = [line.split() for line in s.readlines()]
    s.close() # we don't need to touch the file anymore
    initials = [line[0] for line in parsed]
    # handle bad file content
    # must start with "FFP" -- but allow subsequent tokens on line 1
    if initials[0] != "FFP":
        raise ValueError(f"File {filename} is invalid -- first line does "
                         "not begin with \"FPP\"")
    # if any unacceptable initials are present after FFP, invalidate the file
    # i != 0 bc we know the first initial is FFP if we've made it here
    good_initials = ["CHAR","QUOT","DISP","POLY","EL","#"]
    bad_inds = [i+1 for i, x in enumerate(initials) if (i != 0 and (x not in good_initials))]
    if len(bad_inds) > 0:
        bad_inds_joined = ", ".join(bad_inds)
        raise ValueError(f"File {filename} contains invalid line headers "
                         f"on lines {bad_inds_joined}")
    # CHAR and DISP must introduce exactly 1 line each
    if initials.count("CHAR") != 1:
        if initials.count("CHAR") == 0:
            raise ValueError(f"File {filename} is missing a characteristic "
                             "declaration")
        char_inds = [i+1 for i, x in enumerate(initials) if x == "CHAR"]
        char_inds_joined = ", ".join(char_inds)
        raise ValueError(f"File {filename} contains duplicate characteristic "
                         f"declarations on lines {char_inds_joined}")
    if initials.count("DISP") != 1:
        if initials.count("DISP") == 0:
            raise ValueError(f"File {filename} is missing a display options "
                             "declaration")
        disp_inds = [i+1 for i, x in enumerate(initials) if x == "DISP"]
        disp_inds_joined = ", ".join(disp_inds)
        raise ValueError(f"File {filename} contains duplicate display options "
                         f"declarations on lines {disp_inds_joined}")
    # QUOT is not mandatory, but can't appear more than once
    if initials.count("QUOT") > 1:
        quot_inds = [i+1 for i, x in enumerate(initials) if x == "QUOT"]
        quot_inds_joined = ", ".join(quot_inds)
        raise ValueError(f"File {filename} contains duplicate quotient polynomial "
                         f"declarations on lines {quot_inds_joined}")
    # if QUOT is not present, however, no ELs should be present either
    if ("QUOT" not in initials) and ("EL" in initials):
        el_inds = [i+1 for i, x in enumerate(initials) if x == "EL"]
        el_inds_joined = ", ".join(el_inds)
        raise ValueError(f"File {filename} contains field elements at line(s) "
                         f"{el_inds_joined}, but quotient polynomial "
                         "declaration is missing")
    # if we made it this far, we know that:
    # - CHAR appears exactly once
    # - DISP also appears exactly once
    # - QUOT appears at most once
    # everything else is POLYs and ELs
    li_char = initials.index("CHAR")
    li_disp = initials.index("DISP")
    li_quot = -1
    if "QUOT" in initials:
        li_quot = initials.index("QUOT")
    lis_poly = [i for i, x in enumerate(initials) if x == "POLY"]
    lis_el = [i for i, x in enumerate(initials) if x == "EL"]
    # check all lines for validity BEFORE loading anything in
    # characteristic
    if len(parsed[li_char]) > 2:
        raise ValueError(f"Characteristic declaration on line {li_char+1} "
                         "is too long: expected 1 argument, got "+
                         str(len(parsed[li_char])-1))
    elif len(parsed[li_char]) == 1:
        raise ValueError(f"Characteristic declaration on line {li_char+1} "
                         "is missing the characteristic.")
    # display options
    if len(parsed[li_disp]) < 3:
        raise ValueError(f"Display options declaration on line {li_disp+1} "
                         "is too short: expected 2 arguments, got "+
                         str(len(parsed[li_disp])-1))
    if not validate_disp(parsed[li_disp][1:]):
        raise ValueError(f"Invalid display options declaration on "
                         f"line {li_disp+1}")
    # quotient polynomial
    # len < 4 <=> less than 3 coefficients supplied
    # <=> degree of quotpoly is less than 2
    # <=> no can do
    if "QUOT" in initials and len(parsed[li_quot]) < 4:
        raise ValueError(f"Quotient polynomial declaration on line {li_disp+1} "
                         "is too short: expected 3 or more arguments, got "+
                         str(len(parsed[li_quot])-1))
    # check all polys and els for missing names and/or coeffs
    for i in lis_poly + lis_el:
        # minimum is "POLY" + name + at least one coeff = 3 tokens
        if len(parsed[i]) < 3:
            objtype = "Polynomial" if initials[i] == "POLY" else "Field element"
            raise ValueError(f"{objtype} declaration on line {i+1} is "
                             f"missing a name and/or coefficients")
    # so now we know everything is good
    # clear the current workspace
    print(f"File {filename} validated.")
    dm.mass_delete()
    npf.FieldEl.quotpoly = None
    npf.FieldEl.powers = []
    print("Previous workspace cleared.")
    # and now we load all the shit in
    # if exceptions happen, they get handled further upstream
    # 1. characteristic
    newchar = int(parsed[li_char][1])
    dm.set_characteristic(newchar)
    print(f"Characteristic set to {newchar} successfully.")
    # 2. field, if present
    if li_quot != -1:
        quotcoes = [int(coe) for coe in parsed[li_quot][1:]]
        dm.make("_TMPQP",quotcoes)
        dm.set_field("_TMPQP") # this one prints 
        dm.delete("_TMPQP")
    # 3. display options
    # we don't need to validate them a second time
    update_disp(parse_disp(parsed[li_disp][1:]))
    print("Display options set to:\n" + str(pol.display_cfg))
    # 4. polynomials and field elements
    for i in lis_poly:
        polyname = parsed[i][1]
        polycoes = [int(coe) for coe in parsed[i][2:]]
        dm.make(polyname, polycoes, mode="poly")
        print(f"Polynomial {polyname} loaded.")
    for i in lis_el:
        elname = parsed[i][1]
        elcoes = [int(coe) for coe in parsed[i][2:]]
        dm.make(elname, elcoes, mode="el")
        print(f"Field element {elname} loaded.")