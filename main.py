# This code is used to identify which sections should be excluded from analysis.
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import gc

import header as h
matplotlib.use('Agg')

source_folder = "D:/PD_Participant_Data/LLR_DATA_ANALYSIS_CLEANED/LLR_DATA_PROCESSING_PIPELINE/4_LLR_DATA_SEGMENTATION/NPZ_FILES_BY_TARGET"
save_folder = "D:/PD_Participant_Data/LLR_DATA_ANALYSIS_CLEANED/LLR_DATA_PROCESSING_PIPELINE/4_LLR_DATA_SEGMENTATION/GRAPHS"

if __name__ == '__main__':
    for file in os.listdir(source_folder):
        if file.endswith('.npz'):
            task_number = h.get_task_number(file)
            if (("T1" in file) or ("T2" in file)) & ("V0" in file):
                # Here if file includes task 1 and 2, and if it also is a V0 file, as I'm not studying other pieces
                # of information.
                print(file)
                source_file = source_folder + '/' + file
                file_name = file.split('.')[0]
                # The source file is a npz file. So I need to load in the data and unpack.
                data = np.load(source_file, allow_pickle=True)
                # Unpack the data.
                ragged_list, target_list, target_i = h.load_npz(data)
                # Collect some pieces of information.
                t = target_list[:, h.data_header.index("Time")]
                fx = target_list[:, h.data_header.index("CorrForce_X")]
                fy = target_list[:, h.data_header.index("CorrForce_Y")]
                vx = target_list[:, h.data_header.index("X_Vel")]
                vy = target_list[:, h.data_header.index("Y_Vel")]
                target_num = target_list[:, h.data_header.index("Target_Num")]
                to_from_home = target_list[:, h.data_header.index("To_From_Home")]
                # Plot the data.
                fig = plt.figure(num=1, dpi=100, facecolor='w', edgecolor='w')
                fig.set_size_inches(25, 8)
                plt.suptitle("Identifying Regions to Exclude From Analysis for " + file_name)
                ax1 = fig.add_subplot(211)
                ax2 = fig.add_subplot(212)
                ax1.plot(t, fx, label="Force [N]")
                ax1.plot(t, vy*100, label="Velocity [m/s]")
                ax1.plot(t, target_num, label="Target Number")
                ax1.plot(t, to_from_home, label="To_From_Home")
                ax1.set_title("Y-Axis")
                ax1.set_ylabel("Magnitude")
                ax1.legend()
                ax1.grid()
                ax1.minorticks_on()
                ax2.plot(t, fy, label="Force [N]")
                ax2.plot(t, vx * 100, label="Velocity [m/s]")
                ax2.plot(t, target_num, label="Target Number")
                ax2.plot(t, to_from_home, label="To_From_Home")
                ax2.set_title("Y-Axis")
                ax2.set_ylabel("Magnitude")
                ax2.set_xlabel("Time [s]")
                ax2.legend()
                ax2.grid()
                ax2.minorticks_on()
                # Save the file.
                save_str = save_folder + '/' + file_name
                plt.savefig(fname=save_str)
                fig.clf()
                gc.collect()
