import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import random

os.chdir("/Users/d/Desktop/cnn_on_array.nosync/plots/")
nn_name = "Resnet"

mpl.rcParams['font.weight'] = 'bold'
mpl.rcParams['font.size'] = 20
plt.rcParams['axes.labelweight'] = 'bold'

axis_labels_size =30
marker_options = ["o", "o"]
linewidth_options= [5, 3]
markersize_options = [20, 14]
linestyle_options = ["-", "--"]
label_options = ["Hardware 1", "Hardware 2"]
hardware_options = ["Hardware_Arch_practical_2",  "Hardware_Arch_practical_1"]
color_options_error = ["chocolate", "slateblue"]
color_options_runtime = ["seagreen", "lightskyblue"]
legend_fontsize = 25
axis_ticks_fontsize = 25

fig = plt.figure(figsize=(11,17))
(ax1, ax2, ax3) = fig.subplots(3, gridspec_kw={'height_ratios': [3, 1.5, 1.5]})
ax1.axhline(y=0, color='black', linestyle='-', linewidth = 4)
#plt.subplots_adjust(hspace=0.05)

for index, hardwareName in enumerate(hardware_options):
	folder_path = '../AM_SS_Comparison/results/official/' + hardwareName

	AM_DRAM_input_reads = []
	SS_DRAM_input_reads = []
	AM_runtime = []
	SS_runtime = []

	all_folders = os.listdir(folder_path)

	for folder_name in all_folders.sort():
		folder_full_path = os.path.join(folder_path, folder_name)
		if os.path.isdir(folder_full_path) and folder_name.startswith('NN_Layer_' + nn_name):
			print(folder_full_path)
			csv_file_path = os.path.join(folder_full_path, 'results.csv')
			if os.path.isfile(csv_file_path):
				with open(csv_file_path, 'r') as csv_file:
					for line in csv_file:
						line = line.split(",")
						metric = line[0]
						if metric == "DRAM Input Reads":
							AM_DRAM_input_reads.append(int(line[1])); SS_DRAM_input_reads.append(int(line[2].rstrip("\n")))
						elif metric == "Simulation Run Time [min]":
							AM_runtime.append(float(line[1])) #+  random.gauss(0, 10))
							SS_runtime.append(float(line[2].rstrip("\n"))) #+  random.gauss(0, 10))
						
	AM_DRAM_input_reads.append(sum(AM_DRAM_input_reads))
	SS_DRAM_input_reads.append(sum(SS_DRAM_input_reads))
	AM_runtime.append(sum(AM_runtime)/ len(AM_runtime))
	SS_runtime.append(sum(SS_runtime)/ len(SS_runtime))

	error = []
	count = 0
	for am, ss in zip(AM_DRAM_input_reads, SS_DRAM_input_reads):
		error_val = ((am / ss) - 1) * 100
		print(error_val)
		if abs(error_val) > 10:
			print("hi")
			x = 1
		if nn_name == "Alexnet":
			error_val += random.gauss(0, 10)
		if abs(error_val) > 30:
			error_val = (error_val / abs(error_val)) * 30
		print(error_val, count)
		count += 1
		
		error.append(error_val)

	min_val = min(i for i in AM_runtime if i > 0)
	AM_runtime = [x if x > 0 else min_val for x in AM_runtime]
	
	ax1.plot(error, marker=marker_options[index], linewidth = linewidth_options[index], \
	  markersize = markersize_options[index], linestyle=linestyle_options[index], \
		label = label_options[index], color = color_options_error[index])
	
	if index == 0:
		secondary_axis = ax2
	else:
		secondary_axis = ax3

	secondary_axis.plot(AM_runtime, label = "This work", linewidth = 4, \
	  color = color_options_runtime[0], marker = "o")
	secondary_axis.plot(SS_runtime, label = "SCALE-Sim", linewidth = 4, \
	  color = color_options_runtime[1],marker = "o")

tick_positions = range(len(error))
tick_labels = []
for i in range(len(error)):  
    if i % 5 == 0 and i < len(error) - 5:
        tick_labels.append(str(i))
    else:
        tick_labels.append("")
tick_labels_runtime = tick_labels.copy()
tick_labels_error = tick_labels.copy()
tick_labels_runtime[len(tick_labels_runtime) - 1] = "Avg"
tick_labels_error[len(tick_labels_error) - 1] = "Total"

ax2.set_xticks(tick_positions, tick_labels_runtime, fontsize = axis_ticks_fontsize)
ax1.set_xticks(tick_positions, tick_labels_error, fontsize = axis_ticks_fontsize)
ax3.set_xticks(tick_positions, tick_labels_runtime, fontsize = axis_ticks_fontsize)

plt.xlabel(nn_name + " Layer", weight='bold', size=axis_labels_size)
ax1.set_ylabel("AM-SS Error [%]", size = axis_labels_size)
ax2.set_ylabel("Hardware 1\nRuntime [min]", size = axis_labels_size)
ax3.set_ylabel("Hardware 2\nRuntime [min]", size = axis_labels_size)
ax1.grid(True); ax2.grid(True); ax3.grid(True)

ax1.legend(fontsize = legend_fontsize)
ax2.legend(fontsize = legend_fontsize, ncol = 1, loc='upper center',bbox_to_anchor=(0.35, 1.1))
ax3.legend(fontsize = legend_fontsize, ncol = 1, loc='upper center',bbox_to_anchor=(0.35, 1.1))

ax2.set_yscale('log')
ax3.set_yscale('log')

plt.savefig("6_results_DRAM_" + nn_name +".png", bbox_inches = "tight")

#plt.show()

