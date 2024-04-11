import sys
from pyjls import Reader, SummaryFSR
import matplotlib.pyplot as plt
import matplotlib
import os
import numpy as np
from pathlib import Path
import argparse

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




def read_joulescope_file(jls_file_path):
    if not os.path.exists(jls_file_path):
            print(f"no jsl file found at {anno_file_path}")

    anno_file_path = jls_file_path.rsplit('.', 1)[0] + '.anno.jls'
    start_timestamp, end_timestamp = read_annotations(jls_file_path)

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

    return power_mean, start_timestamp, end_timestamp



def save_plot(name):
    output_dir = Path("./out")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"{name}.pdf"
    plt.savefig(output_file, format='pdf')
    print(f"Plot saved to {output_file}")



def plot_data(power, power2, start_timestamp, end_timestamp, name, show_plot, label):
    fig, ax = plt.subplots(figsize=(8, 5))

    duration_ms = (end_timestamp - start_timestamp) / 1000
    length = min(len(power), len(power2))
    time_range_ms = np.linspace(0, duration_ms, length)

    ax.set_xlabel(r'\textit{t} / ms', fontsize=12, usetex=True)

    if duration_ms > 1000:
        ax.set_xlabel(r'\textit{t} / s', fontsize=12, usetex=True)
        time_range_ms = np.linspace(0, duration_ms / 1000, length)

    ax.set_ylabel(r'\textit{P} / mW', fontsize=12, usetex=True)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.set_ylim(bottom=0, top=max(max(power), max(power2)))
    ax.set_xlim(left=0, right=max(time_range_ms))

    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.tick_params(axis='both', which='major', labelsize=10)

    if len(label) == 0:
        label = [None, None]

    ax.plot(time_range_ms, power[0:length], color='darkblue', label=label[0])

    if power2 is not None:
        ax.plot(time_range_ms, power2[0:length], color='red', label=label[1])

    if label[0] is not None:
        plt.legend()

    plt.tight_layout()

    save_plot(name)

    if show_plot:
        plt.show()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="plot jls files as fancy diagrams")
    parser.add_argument('jls_file', type=str, help="path to jls file")
    parser.add_argument('-o', '--output', type=str, help="name of resulting png file", default="out")
    parser.add_argument('-s', '--show', action='store_true', help="whether the created plot should be shown")
    parser.add_argument('-a', '--add-file', help="addition file")
    parser.add_argument('-l', '--label', help="label for first file", action='append', default=[])
    args = parser.parse_args()

    jls_file_path = args.jls_file

    power, start_timestamp, end_timestamp = read_joulescope_file(jls_file_path)

    power2 = None
    if args.add_file is not None:
        power2, _, _ = read_joulescope_file(args.add_file)

    plot_data(power, power2, start_timestamp, end_timestamp, args.output, args.show, args.label)
