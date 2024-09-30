import argparse
import numpy as np
import pandas as pd

# Parse arguments
parser = argparse.ArgumentParser(
    prog="DSM Builder", description="Builds elements of a DSM from an OPL text file."
)
parser.add_argument("input", help="Input OPL file", type=open)
parser.add_argument("output", help="Output file")
parser.add_argument("matrix", choices=["PO", "PP", "OO"], help="Desired output matrix")
args = parser.parse_args()


class Relation:
    def __init__(self, object, keyword, process):
        self.object = object
        self.keyword = keyword
        self.process = process


# Essentially the OPL contains the following information
# 1. Objects (lines ending in "object")
# 2. Process (lines ending in "process")
# 3. Relations between processes and objects
#       This can be in the form Process-Keyword-Object(s)
#       Keywords are: requires, affects, consumes, yields
#       Or Object(s)-"handles"-Process for Agent relations
#       many-to-one relation ships are comma separated in one line

# Build lists of each item
objects = []
processes = []
relations = []

# Parse the input file
for line in args.input.readlines(False):

    # Incase the input has empty lines
    if line.find(".") == -1:
        continue

    # Remove pesky newlines and trim the leading numbers
    line = line.split(".")[1].strip()

    # Check if the line is an object
    if line.endswith("object"):
        objects.append(line.split(" is ")[0].strip())
        continue

    # Check if the line is a process
    if line.endswith("process"):
        processes.append(line.split(" is ")[0].strip())
        continue

    # Check if this line is a "handles" relationship
    # Object(s)-"handles"-Process
    if line.find(" handles ") != -1:

        # Split on the keyword
        l = line.split(" handles ")
        process = l[1].strip()

        # Check for multiple objects and create a relationship for each one
        for object in [
            x.strip() for x in l[0].replace(" and ", ",").split(",") if x.strip()
        ]:
            relations.append(Relation(object, "handles", process))
        continue

    # If none of these we will assume the line is a relationship
    # Process-Keyword-Object(s)
    keywords = ["affects", "requires", "yields", "consumes"]
    for keyword in keywords:

        # Check if the keyword exists
        if line.find(keyword) != -1:

            # Split on the keyword
            l = line.split(keyword)
            process = l[0].strip()

            for object in [
                x.strip() for x in l[1].replace(" and ", ",").split(",") if x.strip()
            ]:
                relations.append(Relation(object, keyword, process))

# Remove any duplicates and sort
objects = np.unique(np.array(objects, dtype="object"))
processes = np.unique(np.array(processes, dtype="object"))

# Check to make sure there is at least one object and process
if len(objects) == 0 or len(processes) == 0:
    print("Invalid input, exiting.")
    exit()

# Create matrices
po = pd.DataFrame(
    np.empty((len(processes), len(objects)), dtype="object"), processes, objects
)
po_num = pd.DataFrame(np.zeros((len(processes), len(objects))), processes, objects)

# Iterate over all the relations and build the Process-Object Matrix
for r in relations:
    po.loc[r.process, r.object] = r.keyword[0]  # store a letter noting the relationship
    po_num.loc[r.process, r.object] = (
        1  # write a one for doing matrix multiplication later
    )

# Compute the Process-Process Matrix
pp = pd.DataFrame(np.dot(po_num, po_num.transpose()), processes, processes)

# Compute the Object-Obejct Matrix
oo = pd.DataFrame(np.dot(po_num.transpose(), po_num), objects, objects)

print("Processed:")
print(f"{len(objects)} objects")
print(f"{len(processes)} processes")
print(f"{len(relations)} relationships")

# Save the results as a CSV
with open(args.output, "w", newline="") as output_file:

    print(f"Writing {args.matrix} matrix to {args.output}")

    if args.matrix == "PO":
        po.to_csv(path_or_buf=output_file)

    if args.matrix == "PP":
        pp.to_csv(path_or_buf=output_file)

    if args.matrix == "OO":
        oo.to_csv(path_or_buf=output_file)
