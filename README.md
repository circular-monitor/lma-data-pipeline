# lma-data-pipeline

General to dos:
- error handling
- performance optimization
- coding style
- logging
- tests
    + ample test coverage to upgrade python version or dependencies confidently
- sanity checks

## Usage

### Setup

This pipeline is written for Python 3.

Install the requirements:

```
pip install -r requirements.txt
```

#### Windows

On windows, you will run into an error installing the `fiona` dependency. To fix this, first install `gdal` and `fiona` manually. Pick the wheel (`.whl`) file for your version of python from these link:

https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal
https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona

For example, for python 3.8 on a 64 bit computer, download: `GDAL‑3.1.3‑cp38‑cp38‑win_amd64.whl`.

And then install using:

```
pip install GDAL‑3.1.3‑cp38‑cp38‑win_amd64.whl
pip install Fiona‑1.8.17‑cp38‑cp38‑win_amd64.whl
```

Then run:

```
pip install -r requirements.txt
```

### Running

```
python main.py
```

### Adding dependencies

Add the desired dependency to `requirements.txt` manually, then

```
pip install -r requirements.txt
```

Don't use `pip freeze > requirements.txt`, because that will put dependencies of dependencies in `requirements.txt` and they will not be removed on a `pip uninstall`.

# Testing data

Testing data is a file that has the same structure as the data dump we receive from the LMA and is based on the real errors found in the datasets.
Although the data resembles real data and may contain real company names, the fields are randomised, therefore no actual information is revealed.
Testing dataset should contain all known errors and deficiencies of data, therefore every time a new inconsistency has been found,
that hasn't been handled earlier, it should be added as a new line to the testing dataset.

# Input / output

Each module takes the full dataframe, creates new columns with the necessary enhancements, adds them to the end of the original dataframe and returns it.
At the end of each module, a check needs to be made if the length of the input dataframe is the same as the length of the output dataframe.
This rule doesn't apply to the filtering module which reduces the number of rows.
