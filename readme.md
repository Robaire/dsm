Usage: `python create_DSM.py input_file output_file matrix`

- `input_file` must be a syntactically correct OPL text file
- `output_file` is a file path for the output CSV
- `matrix` must be one of:
    - `PO`: Process-Object
    - `PP`: Process-Process
    - `OO`: Object-Object
- `-n, --n_clusters`: The number of clusters to use (default is 8)

Values in the Process-Process matrix represent the number of common Objects between the two processes.
The inverse is true for the Object-Object matrix.

Dependencies:
- [numpy](https://numpy.org/)
- [pandas](https://pandas.pydata.org/)