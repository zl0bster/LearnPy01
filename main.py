import os

# "python pip install numpy"
# COMMAND = "python model_manage.py -x 1800 -y 1000 -file Data/LK1-002.01c.STL.pkl"
# COMMAND = "python model_manage.py -x 1800 -y 1000 -file Data/LK1-002.01c.STL"
# COMMAND = "python model_manage.py -x 1800 -y 1000 -file Data/Dispenser.stl"
# COMMAND = "python model_manage.py -x 1800 -y 1000 -file Data/Dispenser.stl.pkl"
# COMMAND = "python model_manage.py -x 1800 -y 1000 -file Data/LK1-003.00.02.STL"
# COMMAND = "python model_manage.py -x 1800 -y 1000 -file Data/LK1-003.00.02.STL.pkl"
COMMAND = "python model_manage.py -x 1800 -y 1000 -file Data/TH1-01.01.01.STL.pkl"
# COMMAND = "python model_manage.py -x 1800 -y 1000 -file Data/TH1-01.01.01.STL"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    os.system(command=COMMAND)
