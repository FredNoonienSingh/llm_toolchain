# LLM-Based Document Comparison Toolchain

This project implements a simplified LLM-based toolchain for comparing supplier offers against a bill of quantities (LV). It uses Ollama for local LLM inference and processes XML and TXT files to extract relevant data.

## Overview

The toolchain reads an LV from an XML file (`LV.X83`) and a supplier offer from a TXT file (`Angebot_Lieferant.txt`). It then uses an LLM to compare corresponding items from both documents and generates a table indicating whether the offers match.

## Requirements

* Python 3.x
* Ollama (for local LLM inference)
* Required Python libraries:
    * `pandas`
    * `lxml`
    * `ollama`

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [repository_url]
    cd [repository_directory]
    ```
2.  **Install dependencies:**
    ```bash
    pip install -e .
    ```
    (This will install the package and its dependencies in editable mode.)
3.  **Install Ollama:** Follow the instructions on the [Ollama website](https://ollama.com/) to install Ollama.
4.  **Create the LLM Model:**
    * Navigate to the `toolchain/modelfiles/` directory.
    * Create a model using the provided modelfile:
        ```bash
        ollama create toolchain_model -f model
        ```

## Usage

1.  **Prepare Input Files:**
    * Place your XML file (`LV.X83`) and TXT file (`Angebot_Lieferant.txt`) in the `data/` directory.
2.  **Run the Toolchain:**
    * You can run the toolchain from the command line:
        ```bash
        python run.py data/LV.X83 data/Angebot_Lieferant.txt output.xls
        ```
    * Alternatively, you can use the provided Jupyter Notebook (`toolchain_notebook.ipynb`) to run the toolchain interactively.
3.  **View Output:**
    * The results will be written to an Excel file (`output.xls`) in the current directory.

## Code Structure

* `run.py`: Main script for running the toolchain from the command line.
* `toolchain/`: Contains the toolchain modules.
    * `llm.py`: Implements the `LLM` class for interacting with Ollama.
    * `file_operations.py`: Implements file I/O and data extraction.
    * `common.py`: Contains common utilities (e.g., logger).
    * `modelfiles/`: Contains the Ollama model definition.
* `data/`: Contains example input files.
* `toolchain_notebook.ipynb`: Jupyter Notebook for interactive use.
* `setup.py`: Packaging information.

## LLM Model

The LLM model is defined in `toolchain/modelfiles/model`. It uses the `llama3.2` base model with specific parameters for temperature, top-p, and top-k.

## Output

The toolchain generates an Excel file (`output.xls`) containing a table with the following columns:

* `is_correct`: A boolean indicating whether the offer is correct.
* `llm_feedback`: A concise explanation from the LLM about the comparison result.

## Notes

* This is a simplified toolchain and may require further refinement for production use.
* Ensure that Ollama is running before executing the toolchain.
* The prompts used for the LLM can be adjusted to improve the accuracy of the results.
* The project is packaged using setuptools and is installable using pip.