This is a calculation system for polynomials over finite fields. It stores and calculates with polynomials in memory as the user enters commands through a text-based interface.

# Currently supported features
## General
- `setchar`: Set the base field characteristic, i.e. the number modulo which the coefficients of all polynomials are taken. Default is 7, can be set to any prime.
- `list`: View all available commands in-program.
- `help`: View usage and info about a particular command, group of commands, or general information.
## Data management
- `create`, `delete`, `update`, `rename`, `copy`: Manipulate polynomials in memory.
- `show`, `showall`: Display one polynomial, or all stored in memory, on the screen.
## Arithmetic
- `add`, `subtract`, `multiply`, `power`: Ring operations.
- `eval`: Evaluate a polynomial at a point.
- `modulo`: Reduce one polynomial modulo another.
- `eucdiv`: Perform Euclidean division.
- `eea`: Perform the extended Euclidean algorithm to find the GCD of two polynomials along with Bézout coefficients.
# Planned features
## Data management
- File I/O: Save current workspace to a file, load polynomials in from a file (overwriting and additive)
- For multi-output commands, allow the use of `_` in lieu of an output name to discard some outputs
- Impose restrictions on what strings can be used as polynomial names
## Arithmetic
- Irreducibility and primitivity checks for polynomials
- Factorization of polynomials
- Calculations in non-prime finite fields
