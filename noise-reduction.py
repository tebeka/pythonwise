# View notebook at http://bit.ly/191MRIN
from matplotlib import pyplot as plt
import numpy as np

values = np.random.binomial(1000, 0.5, 1000)
plt.hist(values, bins=20)  # We'll get the below before the chart
# (array([   3.,    3.,    7.,   23.,   39.,   46.,   75.,   94.,   94.,
#         118.,  121.,  104.,   82.,   66.,   45.,   46.,   18.,    8.,
#           6.,    2.]),
#  array([ 454.  ,  458.65,  463.3 ,  467.95,  472.6 ,  477.25,  481.9 ,
#         486.55,  491.2 ,  495.85,  500.5 ,  505.15,  509.8 ,  514.45,
#         519.1 ,  523.75,  528.4 ,  533.05,  537.7 ,  542.35,  547.  ]),
#  <a list of 20 Patch objects>)

# Option 1: Use assignment
_ = plt.hist(values, bins=20)  # Remove noise

# Option 2: Dummy last expression
plt.hist(values, bins=20)
None # Remove noise
