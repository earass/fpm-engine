Following are the files details:

pokec/cache/files: contains cache files (Add the 'Cleaned_pokec_dataset.parquet' file in this directory)
pokec/data/interface.py: code for reading the data
pokec/data/preprocess.py: code for preprocessing the data
pokec/engine/fpm.py: Trigger methods for FPM algorithms
pokec/engine/pcp_miner: code for Colossal Pattern mining obtained from https://github.com/GENU05/mining-colossal-patterns-in-high-dimensional-databases
pokec/explore/plots: charts are saved in this directory
pokec/explore/__init__.py: code for data exploration and generating visualizations
pokec/explore/viz.py: Visualization utility functions imported in exploration module

run.py: Imports all the above modules and triggers the pipeline.

requirements.txt: contains all the packages that need to installed prior to running this project

In order to run the code, just run the run.py file.

Input Dataset link: https://drive.google.com/file/d/1WbWDEyuBB5kHF50WYiDLImKrdYjmG7F5/view?usp=sharing
The dataset must be placed in dir: pokec/cache/files
If you want to run it for testing, a small sample file is present in directory. You can set the read_sample flag as True to run it on the sample dataset

Contact:
i191254@nu.edu.pk
