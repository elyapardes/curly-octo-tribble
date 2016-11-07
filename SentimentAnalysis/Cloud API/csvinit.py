import numpy as np
import csv

csvarr = np.zeros((9, 3))

with open("CallsToProcess/output.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(csvarr)