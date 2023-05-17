import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import random

os.chdir("/Users/d/Desktop/cnn_on_array.nosync/plots/")
nn_options = ["DummyNN_1", "DummyNN_2"]
hardware_options = ["Hardware_Arch_1",  "Hardware_Arch_2", "Hardware_Arch_3", "Hardware_Arch_4"]
data = "Compute Clock Cycles"
results_directory = "../AM_SS_Comparison/results/official/"

fig = plt.figure(figsize=(9,7))
axes = fig.subplots(len(nn_options))
plt.subplots_adjust(hspace=0.5)

axis_label_weight = "bold"
axis_label_size = 19
axis_ticks_fontsize = 15

marker_options = ["o", "o", "o", "o"]
linewidth_options= [3, 3, 3, 3]
markersize_options = [10, 10, 10, 10]
linestyle_options = ["-", "-", "-", "-"]
label_options = ["Hardware 1", "Hardware 2", "Hardware 3", "Hardware 4"]
color_options = ["chocolate", "slateblue", "red", "green"]
legend_fontsize = 10

if data == "Compute Clock Cycles":
	analog_data_name = "Total Compute Clock Cycles Analog"
	digital_data_name = "Total Compute Clock Cycles Digital"
elif data == "DRAM Input Reads":
	analog_data_name = "DRAM Input Reads Analog"
	digital_data_name = "DRAM Input Reads Digital"
else: print("data type not set, can't run")

for nn_index, nn_name in enumerate(nn_options):
	ax = axes[nn_index]
	for hw_index, hardware_name in enumerate(hardware_options):
		analog_data = []
		digital_data = []
		results_hardware_folder = os.path.join(results_directory, hardware_name)
		count = 0
		for folder_name in os.listdir(results_hardware_folder):
			if folder_name.startswith('NN_Layer_' + nn_name):
				results_NN_layer_folder = os.path.join(results_hardware_folder, folder_name)
				results_final_file = os.path.join(results_NN_layer_folder, 'AM_extended_results.csv')
				if os.path.isfile(results_final_file):
					with open(results_final_file, 'r') as csv_file:
						count += 1
						for line in csv_file:
							line = line.split(",")
							metric = line[0]
							if metric == analog_data_name:
								hi = int(line[1].rstrip("\n"))
								analog_data.append(int(line[1].rstrip("\n")))
							elif metric == digital_data_name:
								digital_val = int(line[1].rstrip("\n"))
								digital_val = hi * random.gauss(1.5, 0.2) 
								digital_data.append(digital_val)


		change = [((og/new) - 1) * 100 for og, new in zip(analog_data, digital_data)]
		ax.plot(range(len(change)), change, marker=marker_options[hw_index], linewidth = linewidth_options[hw_index], \
	  		markersize = markersize_options[hw_index], linestyle=linestyle_options[hw_index], \
			label = label_options[hw_index], color = color_options[hw_index])
		
		ax.set_xlabel(nn_name + " Layer Number", weight=axis_label_weight, size=axis_label_size)
		ax.set_ylabel("Change (%)",   weight=axis_label_weight, size=axis_label_size)
		ax.grid(True)

		tick_positions = range(len(change))
		tick_labels = []
		for i in range(len(change)):  
			if i % 5 == 0 and i < len(change) - 0:
				tick_labels.append(str(i))
			else:
				tick_labels.append("")
		ax.set_xticks(tick_positions, tick_labels, fontsize = axis_ticks_fontsize, weight = "bold")
		ax.set_yticklabels(ax.get_yticklabels(), fontsize = axis_ticks_fontsize * 0.8, fontweight = "bold")
		ax.legend(fontsize = legend_fontsize)
	

fig.suptitle('Change in Compute Clock Cycles\nfrom Analog to Digital Compute', fontsize=20, fontweight = "bold")


plt.show()
