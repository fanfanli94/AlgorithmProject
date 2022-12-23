### Prerequisites and Dependencies
Note that you also need to install `networkx` package to run `LS1` and `BnB` code. To add that into your python, type the following commands in the terminal
```
pip install networkx
```

### Running the code
To run the code, follow the following steps:
1. Under the directory containing `DATA` folder and `main.py, Approx.py, LS1.py, LS2.py` files
2. Enter the commands to execute the code, the following is an example of that which run the `Approx` algorithm on the `email.graph` graph file, `600` is the cutoff time if needed for some algorithm and `1045` is a random seed which can be any number:
```
python main.py -inst email.graph -alg Approx -time 600 -seed 1045
```        
(FYI, you can run the bash file to run all cases for Approx algorithm)

3. You can find the output files under `Output` folder
