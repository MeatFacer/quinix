import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


""""
Implementing a model a described in the link below would probably work well for this type of data
https://nbviewer.jupyter.org/github/srnghn/ml_example_notebooks/blob/master/Predicting%20Yacht%20Resistance%20with%20K%20Nearest%20Neighbors.ipynb
For this model to work we would probably need to clean some of the data such as turning Stevedorenames into integers. 
We could then try and fit the model, and play around with the type of input we provide the model. Most likely not all data is useful some we might find a better solution with less input columns.
"""
predictionTypes = ["discharge1", "load1", "discharge2", "load2", "discharge3", "load3", "discharge4", "load4",]
vesselData = pd.read_csv('VesselData.csv')
print(vesselData)