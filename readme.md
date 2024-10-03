A tool to generate a [Design Structure Matrix](https://en.wikipedia.org/wiki/Design_structure_matrix) from an [Object Process Model](https://en.wikipedia.org/wiki/Object_Process_Methodology) graph.

Usage: `python create_DSM.py --help`

Values in the Process-Process matrix represent the number of common Objects between the two processes.
The inverse is true for the Object-Object matrix.

By default the output is ordered alphabetically.
Alternatively the output can be clustered using [spectral clustering](https://en.wikipedia.org/wiki/Spectral_clustering).
Cluster labels can be saved as a separate output. 
If an arbitrary ordering of the output is desired a file containing all the elements in the preferred order can be provided as an input.

Dependencies:
- [numpy](https://numpy.org/)
- [pandas](https://pandas.pydata.org/)
- [scikit-learn](https://scikit-learn.org/)