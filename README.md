This is a calculation system for polynomials over finite fields. It stores and calculates with polynomials in memory as the user enters commands through a text-based interface.

# Instructions

Run the `main.py` file.

# Currently supported features

## General
- `setchar`: Set the base field characteristic, i.e. the number modulo which the coefficients of all polynomials are taken. Default is 7, can be set to any prime.
	- Changing the characteristic also deletes all currently stored polynomials in memory.
- `char`: View the current base field characteristic.
- `setfield`: Initialize a non-prime field via a primitive polynomial.
	- The order of the field is `p^n`, where `p` is the field characteristic and `n` is the degree of the polynomial. 
	- The polynomial must be of degree at least 2.
- `list`: View all available commands in-program.
- `help`: View usage and info about a particular command, group of commands, or general information.
- `displayoptions` (alias `dpo`): Control how polynomials are displayed on the screen. Currently supported are two toggleable options:
	- `deg`: Term order -- either in ascending order by degree, or in descending order by degree.
	- `bal`: Coefficient display -- coefficients normalized either to between `0` and `p-1` ("unbalanced"), or to betweeen `-(p-1)/2` and `(p-1)/2` ("balanced"). Here `p` denotes the characteristic of the base field. Ignored in characteristic 2!
## Data management
- `create`, `delete` (alias `del`), `deleteall` (alias `flush`), `update`, `rename`, `copy`: Manipulate polynomials and field elements in memory.
	- `delete` can delete multiple objects at a time.
	- `deleteall` can delete all stored polynomials, all stored field elements, or everything.
	- `createbinary` (alias `cbin`): In characteristic 2, create a polynomial or field element by specifying which exponents appear as terms.
		- Available only in characteristic 2.
- `show`: Display one polynomial or field element on the screen.
- `showall`: Display all stored polynomials, all stored field elements, or both, on the screen.
	- If field elements are displayed, the field's defining polynomial is too.
	- Polynomials are printed with powers of `x`, and field elements are printed with powers of `a`.
		- `a` is the image of `x` under the natural projection `F_p[x] -> GF(p^n)`.
## Arithmetic
- Universal commands:
	- `add`, `subtract` (alias `sub`), `multiply` (alias `mul`), `power` (alias `pow`): Ring operations.
		- `add` and `multiply` can operate on many polynomials at a time (but at least 2 operands must be supplied).
		- These support both polynomials and field elements, but type-mixing is not allowed.
- Field element-only commands:
	- `divide` (alias `div`): Divide two field elements.
- Polynomial-only commands:
	- `eval`: Evaluate a polynomial at a point.
	- `modulo` (alias `mod`): Reduce one polynomial modulo another.
	- `eucdiv`: Perform Euclidean division.
	- `eea`: Perform the extended Euclidean algorithm to find the GCD of two polynomials along with Bézout coefficients.
## Number-theoretic properties
- Polynomial properties:
	- `degree` (alias `deg`): Self-explanatory.
	- `irred`: Checks if a polynomial is irreducible using Rabin's test. Has `reason` option to view the reason as found by the checker:
		- Constant -- NOT irreducible
		- Linear -- irreducible
		- Has a root (equivalently, a linear factor) -- NOT irreducible
		- Has a repeated factor -- NOT irreducible
		- Fails Rabin's test -- NOT irreducible
		- Passes Rabin's test -- irreducible
	- `prim`: Checks if a polynomial is primitive.
- Field element properties:
	- `dlog`: Discrete logarithm to base `a`, where `a` is the generator of the field.
	- `order`: Order in the multiplicative group of `GF(p^n)`. 
# Planned features

## General
- Name validation: forbid the use of certain names for polynomial creation
## Data management
- File I/O: Save current workspace to a file, load polynomials in from a file (overwriting and additive)
- For multi-output commands, allow the use of `_` in lieu of an output name to discard some outputs
- Impose restrictions on what strings can be used as polynomial names
## Arithmetic
- Factorization of polynomials