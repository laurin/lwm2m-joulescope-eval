import sys
from pyjls import Reader, SummaryFSR
import matplotlib.pyplot as plt
import matplotlib
import os
import numpy as np

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
})

def read_annotations(jls_file_path):
    anno_file_path = jls_file_path.rsplit('.', 1)[0] + '.anno.jls'
    annotation_timestamps = []
    
    with Reader(anno_file_path) as r:
        if os.path.exists(anno_file_path):
                def annotation_callback(timestamp, y, annotation_type, group_id, data):
                    annotation_timestamps.append(timestamp)
                    return False

                r.annotations(1, 0, annotation_callback)
        else:
            print(f"no annotation file found at {anno_file_path}")

    return annotation_timestamps




def read_joulescope_file(jls_file_path, start_timestamp, end_timestamp):
    with Reader(jls_file_path) as r:
        signal = r.signal_lookup('power').signal_id
        sr = r.signal_lookup('power').sample_rate 

        # DIY calculate because timestamp_to_sample_id does not seem to work
        start_sample_id = round((start_timestamp * sr) / 1000000)
        end_sample_id = round((end_timestamp * sr) / 1000000)

        length = end_sample_id - start_sample_id
        increment = round(length / 1000)
        power_stats = r.fsr_statistics(signal, start_sample_id, increment, round(length/increment))
        power_mean = power_stats[:, SummaryFSR.MEAN]

    return power_mean




def plot_data(power, start_timestamp, end_timestamp):
    fig, ax = plt.subplots(figsize=(8, 5))

    duration_ms = (end_timestamp - start_timestamp) / 1000
    time_range_ms = np.linspace(0, duration_ms, len(power))

    ax.set_xlabel(r'\textit{t} / ms', fontsize=12, usetex=True)

    if duration_ms > 1000:
        time_range_ms = np.linspace(0, duration_ms / 1000, len(power))
        ax.set_xlabel(r'\textit{t} / s', fontsize=12, usetex=True)

    ax.set_ylabel(r'\textit{P} / mW', fontsize=12, usetex=True)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.tick_params(axis='both', which='major', labelsize=10)

    ax.plot(time_range_ms, power, color='darkblue')
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <path_to_joulescope_file>")
        sys.exit(1)

    jls_file_path = sys.argv[1] 
    if not os.path.exists(jls_file_path):
            print(f"no jsl file found at {anno_file_path}")

    annotation_timestamps = read_annotations(jls_file_path)
    
    if len(annotation_timestamps) == 2:
        start_timestamp, end_timestamp = annotation_timestamps
        power = read_joulescope_file(jls_file_path, start_timestamp, end_timestamp)
        plot_data(power, start_timestamp, end_timestamp)
    else:
        print("no dual annotations found")
