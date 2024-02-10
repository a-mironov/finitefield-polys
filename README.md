This is a calculation system for polynomials over finite fields. It stores and calculates with polynomials in memory as the user enters commands through a text-based interface.

# Currently supported features

## General
- `setchar`: Set the base field characteristic, i.e. the number modulo which the coefficients of all polynomials are taken. Default is 7, can be set to any prime.
	- Changing the characteristic also deletes all currently stored polynomials in memory.
- `list`: View all available commands in-program.
- `help`: View usage and info about a particular command, group of commands, or general information.
- `displayoptions` (alias `dpo`): Control how polynomials are displayed on the screen. Currently supported are two toggleable options:
	- `deg`: Term order -- either in ascending order by degree, or in descending order by degree.
	- `bal`: Coefficient display -- coefficients normalized either to between `0` and `p-1` ("unbalanced"), or to betweeen `-(p-1)/2` and `(p-1)/2` ("balanced"). Here `p` denotes the characteristic of the base field. Ignored in characteristic 2!
## Data management
- `create`, `delete` (alias `del`), `deleteall` (alias `flush`), `update`, `rename`, `copy`: Manipulate polynomials in memory.
	- `delete` can delete multiple polynomials at a time.
- `show`, `showall`: Display one polynomial, or all stored in memory, on the screen.
## Arithmetic
- `add`, `subtract` (alias `sub`), `multiply` (alias `mul`), `power` (alias `pow`): Ring operations.
	- `add` and `multiply` can operate on many polynomials at a time (but at least 2 operands must be supplied).
- `eval`: Evaluate a polynomial at a point.
- `modulo` (alias `mod`): Reduce one polynomial modulo another. Alias `mod`.
- `eucdiv`: Perform Euclidean division.
- `eea`: Perform the extended Euclidean algorithm to find the GCD of two polynomials along with Bézout coefficients.
## Number-theoretic properties
- `degree` (alias `deg`): Displays the degree of a polynomial on the screen.
- `irred`: Checks if a polynomial is irreducible using Rabin's test. Has `reason` option to view the reason as found by the checker:
	- Constant -- NOT irreducible
	- Linear -- irreducible
	- Has a root (equivalently, a linear factor) -- NOT irreducible
	- Has a repeated factor -- NOT irreducible
	- Fails Rabin's test -- NOT irreducible
	- Passes Rabin's test -- irreducible

# Planned features

## General
- Name validation: forbid the use of certain names for polynomial creation
## Data management
- File I/O: Save current workspace to a file, load polynomials in from a file (overwriting and additive)
- For multi-output commands, allow the use of `_` in lieu of an output name to discard some outputs
- Impose restrictions on what strings can be used as polynomial names
## Arithmetic
- Primitivity check for polynomials
- Factorization of polynomials
- Calculations in non-prime finite fields
