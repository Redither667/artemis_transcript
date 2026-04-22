# Artemis transcript

Artemis transcript project is targeted at transforming artemis `.ast` files into human-readable scripts in different
formats including `.docx` and `.md`.

The project is currently under early development, so there may be many bugs. Please report them in github. Improvement
suggestions are also welcomed.

## How to use

### Basic usage
You need to get an instance of `OutputFuncSet` and pass it to function `parse_ast`. You may refer to the test functions
in `main.py`.

### Custom behavior
Inherit `OutputFuncSet` for customized output. Pass an instance of `ParseOption` to `parse_ast` for adjustments.

## Further development

More functionality will be added. Please contribute to the project if you like.

To enhance efficiency and make the code cleaner, the project will be rewritten in a mixture of Rust and Python.
Main logic will be written in Rust and extendable options will be available in both Rust and Python. (Python is included
specifically for `.docx` output)