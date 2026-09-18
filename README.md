# DocDocPy

**AI-powered, source-preserving documentation for Python code.**

DocDocPy is a command-line tool that automatically generates **Google-style docstrings** for Python code using an LLM, while keeping control of your source code in the hands of the tool—not the model.

Instead of asking an LLM to rewrite your entire Python file, DocDocPy extracts the code elements that need documentation, sends only the relevant information to the model, receives documentation, and inserts the generated docstrings back into the original source.

The result is automated documentation without asking an AI model to reconstruct your code.

> **Status:** Experimental
> **Python:** 3.10+
> **LLM provider:** Groq
> **Current model:** `openai/gpt-oss-120b`

---

## Why DocDocPy?

Generating documentation manually can be tedious, especially when working with large Python codebases.

A straightforward approach to AI-generated documentation is to send an entire function or file to an LLM and ask it to return the documented code. This introduces an unnecessary risk: the model may accidentally change code while generating the documentation.

DocDocPy takes a different approach.

### Source preservation by design

The LLM is responsible for **generating documentation only**.

DocDocPy is responsible for **modifying the source file**.

This separation means the model does not need to reconstruct your functions, classes, imports, or other Python code. The original source is parsed and the generated documentation is inserted programmatically.

```text
Python source
     │
     ▼
 Parse source code
     │
     ▼
 Find documentable objects
     │
     ▼
 Send documentation request to LLM
     │
     ▼
 Receive docstrings
     │
     ▼
 Insert docstrings into original source
     │
     ▼
 Updated Python file
```

---

## Features

* Generate Python docstrings automatically using AI
* Google-style docstrings
* Source-preserving documentation workflow
* Supports:

  * Functions
  * Classes
  * Methods
  * Nested/sub-functions
  * Nested/sub-classes
  * `__init__` methods
* Processes multiple documentation targets efficiently
* Uses Groq as the current LLM provider
* Uses `openai/gpt-oss-120b`
* Secure first-run API-key setup
* Stores your API key locally on your computer
* Simple command-line interface
* No configuration file setup required from the user

---

## Installation

Install DocDocPy directly from PyPI:

```bash
pip install docdocpy
```

Verify the installation:

```bash
docdocpy --help
```

---

## Quick Start

Point DocDocPy at a Python file:

```bash
docdocpy my_file.py
```

On the first run, DocDocPy will ask for your **Groq API key**.

Your key is stored locally on your computer so you don't need to enter it every time you use DocDocPy.

After setup, simply run:

```bash
docdocpy my_file.py
```

DocDocPy will analyze the Python file, generate documentation for supported objects, and insert the resulting docstrings directly into the file.

---

## Example

### Before

```python
def calculate_total(price, quantity, discount=0):
    subtotal = price * quantity
    return subtotal - discount
```

Run:

```bash
docdocpy shop.py
```

### After

```python
def calculate_total(price, quantity, discount=0):
    """Calculate the final price after applying a discount.

    Args:
        price: The price of a single item.
        quantity: The number of items.
        discount: The discount amount to subtract from the subtotal.

    Returns:
        The final calculated price after the discount.
    """
    subtotal = price * quantity
    return subtotal - discount
```

The important distinction is that the LLM generates the **docstring**, while DocDocPy inserts it into the original function.

---

## Supported Python Code

DocDocPy currently supports documentation of:

### Functions

```python
def calculate_area(width, height):
    ...
```

### Classes

```python
class UserManager:
    ...
```

### Methods

```python
class UserManager:
    def create_user(self, name):
        ...
```

### Nested functions

```python
def process_data(data):

    def clean_data(value):
        ...
```

### Nested classes

```python
class Application:

    class Configuration:
        ...
```

### `__init__`

```python
class User:

    def __init__(self, name, age):
        ...
```

DocDocPy is designed to discover these objects from the Python source rather than relying on simple text matching.

---

## How It Works

DocDocPy deliberately separates **code analysis**, **documentation generation**, and **source modification**.

### 1. Parse

The Python source is parsed to identify supported functions, classes, and methods.

### 2. Extract

Relevant information about each object is extracted for documentation generation.

### 3. Generate

The extracted information is sent to the Groq API.

The current model is:

```text
openai/gpt-oss-120b
```

The model is instructed to generate **documentation only**, rather than returning reconstructed Python code.

### 4. Validate

The response is checked so that generated documentation can be associated with the correct Python object.

### 5. Insert

DocDocPy inserts the generated docstrings into the original source programmatically.

This is the core of the source-preserving approach.

---

## API Key

DocDocPy currently supports **Groq API keys only**.

On the first invocation that requires the API:

```bash
docdocpy my_file.py
```

DocDocPy prompts you for your API key.

The key is stored locally using the operating system's appropriate application configuration directory through `platformdirs`.

You therefore do not need to:

* Put your API key inside your Python files
* Add it to the DocDocPy package
* Enter it every time you run the tool

Support for additional LLM providers is planned for future versions.

---

## Current Limitations

DocDocPy is currently **experimental**, so its interface and behavior may change as development continues.

The current version intentionally keeps the interface simple.

At the moment:

* Groq is the only supported LLM provider.
* Google is the only supported documentation style.
* The input Python file is modified directly.
* There is currently no output-file option.
* There is currently no command-line option for selecting a documentation style.
* Additional documentation targets and capabilities are planned for future releases.

Always review generated documentation before committing significant changes to a codebase.

---

## Roadmap

DocDocPy is still evolving. Planned functionality includes:

* [ ] Support for additional LLM providers
* [ ] Additional documentation styles

  * [ ] NumPy
  * [ ] Sphinx
  * [ ] Other commonly used Python documentation formats
* [ ] Output-file support
* [ ] Documentation-only / selective targets
* [ ] Additional Python constructs
* [ ] More configuration options
* [ ] Improved control over documentation generation
* [ ] Additional CLI options

The roadmap may change as the project develops and user feedback is incorporated.

---

## Development

Clone the repository and install the project locally:

```bash
git clone <repository-url>
cd docdocpy
pip install -e .
```

Install development dependencies if provided by the project:

```bash
pip install -e ".[dev]"
```

Run the CLI:

```bash
docdocpy my_file.py
```

---

## Project Philosophy

DocDocPy is built around a simple principle:

> **Let AI write the documentation. Don't let AI rewrite your code.**

Large language models are useful for understanding code and producing natural-language explanations. They do not need to be responsible for reconstructing the source code just to add a docstring.

By separating these responsibilities, DocDocPy aims to make AI-assisted documentation more predictable and safer to use.

---

## Contributing

DocDocPy is experimental and open to contributions.

If you find a bug, have an idea, or want to improve the documentation or implementation, feel free to open an issue or submit a pull request.

When contributing, please keep the project's core principle in mind:

**The generated documentation should not require the LLM to rewrite the user's source code.**

---

## License

This project is licensed under the **[MIT License](LICENSE)**.

---

## Author

**Emmanuel Ebi-Fredrick**

If you find DocDocPy useful, consider giving the project a ⭐ on GitHub.
