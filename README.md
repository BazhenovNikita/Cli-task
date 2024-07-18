# Package Comparator

This project provides a utility to compare binary packages between two branches of the ALT Linux repository.

## Features

- Fetches package lists from branches `sisyphus` and `p10`.
- Compares package lists and outputs the results in JSON format.
- The JSON output includes:
  - Packages present in `p10` but not in `sisyphus`.
  - Packages present in `sisyphus` but not in `p10`.
  - Packages with a higher version in `sisyphus` compared to `p10`.
- Comparison is done for each supported architecture (field `arch` in the response).

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/package_comparator.git
    cd package_comparator
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To compare packages between `sisyphus` and `p10` branches, run:

```bash
python -m main.cli p10 sisyphus