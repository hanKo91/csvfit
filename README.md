# csvfit

A collection of simple command line tools for parameter identification/curve-fitting data stored in csv files.

Can also be included as a module like:
```python
from fit import fitpt, fitarx, util
```

## Install

```python
pip install .
```

## Usage
```
Usage: fitpt [OPTIONS]

Options:
  -s, --show             Show plots
  -t, --type TEXT        PTn type: PT1, PT2
  -c, --columns TEXT     Name of the columns
  -o, --outdir PATH      Directory to store output artifacts
  -e, --eventspath PATH  Path to csv file with event data   
  -d, --datapath PATH    Path to csv file with target data  
  --help                 Show this message and exit. 
```
**fitpt** is using a configuration file. This is a csv-file
that specifies which parts of the data should be taken for parameter identification.
Take a look at test/example/events_*.csv in combination with the attached example data.csv.

```
Usage: fitarx [OPTIONS]

Options:
  -s, --show           Show plots
  -c, --columns TEXT   Name of the columns, last one is by default the system
                       output
  -o, --outdir PATH    Directory to store output artifacts
  -d, --datapath PATH  Path to csv file with target data
  --help               Show this message and exit.
```

## Test
```python
python -m unittest -v test.test
```