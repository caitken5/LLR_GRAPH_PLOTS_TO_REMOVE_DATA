import sys
import numpy as np

data_header = ['Time', 'Des_X_Pos', 'Des_Y_Pos', 'X_Pos', 'Y_Pos', 'OptoForce_X', 'OptoForce_Y', 'OptoForce_Z',
               'OptoForce_Z_Torque', 'Theta_1', 'Theta_2', 'Fxy_Mag', 'Fxy_Angle', 'CorrForce_X', 'CorrForce_Y',
               'Target_Num', 'X_Vel', 'Y_Vel', 'Vxy_Mag', 'Vxy_Angle', 'Dist_From_Target', 'Disp_Btw_Pts', 'Est_Vel',
               'To_From_Home', 'Num_Prev_Targets', 'Resistance']


def get_task_number(file_name):
    if "T1" in file_name:
        task = 1
    elif "T2" in file_name:
        task = 2
    elif "T3" in file_name:
        task = 3
    elif "T4" in file_name:
        task = 4
    else:
        my_str = "Task name wasn't found, file_name: " + file_name + ", exiting program."
        sys.exit(my_str)
    return task


def load_npz(npz_file):
    # Assume that each of the npz files contains two pieces of information: the data to be unpacked and the unpacking indices.
    my_list = npz_file.files
    data = npz_file[my_list[0]]
    counter = npz_file[my_list[1]]
    sep_row = np.cumsum(counter)
    # Define an object that the arrays can be loaded into, noting that they are ragged because the number of rows may differ each time.
    ragged_list = [data[0:sep_row[0], :]]  # Append the first set of data.
    for j in range(len(counter)-1):
        ragged_list.append(data[sep_row[j]:sep_row[j+1], :])
        # Since the list values for each array is calculated, the last row in the array is included in the calculation
        # and a separate line to append the last piece of data from a start to end point is not needed.
    return ragged_list, data, counter
