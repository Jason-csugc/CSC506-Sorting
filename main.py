import tkinter as tk
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def time_function(func, arr):
    start = time.perf_counter()
    func(arr.copy())
    return time.perf_counter() - start

def run_analysis():
    sizes = [100, 500, 1000, 2000]
    algorithms = {
        'Bubble Sort': bubble_sort,
        'Merge Sort': merge_sort
        }

    results = []
    for size in sizes:
        for name, func in algorithms.items():
            for run in range(2):
                arr = random.sample(range(size * 10), size)
                exec_time = time_function(func, arr)
                results.append({'Algorithm': name, 'Size': size, 'Time (s)': exec_time})

    df = pd.DataFrame(results)
    display_results(df)

def on_closing():
            print("Window is closing")
            root.destroy()
            sys.exit()

def display_results(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    avg_df = df.groupby(['Algorithm', 'Size']).mean().reset_index()
    for alg in avg_df['Algorithm'].unique():
        data = avg_df[avg_df['Algorithm'] == alg]
        ax.plot(data['Size'], data['Time (s)'], label=alg, marker='o')
    ax.set_title("Sorting Time Complexity")
    ax.set_xlabel("Input Size")
    ax.set_ylabel("Time (s)")
    ax.legend()
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    table_data = avg_df.pivot(index='Size', columns='Algorithm', values='Time (s)').round(6)

    complexity_map = {
        "Bubble Sort": "O(n²)",
        "Merge Sort": "O(n log n)"
    }

    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, "Average Execution Time Table (in seconds):\n\n")
    text_box.insert(tk.END, table_data.to_string())
    text_box.insert(tk.END, "\n\nTheoretical Time Complexities:\n")
    for alg, comp in complexity_map.items():
        text_box.insert(tk.END, f"{alg}: {comp}\n")


root = tk.Tk()
root.title("Sorting Algorithm Analyzer")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

btn = tk.Button(root, text="Run Analysis", command=run_analysis)
btn.pack(pady=10)

text_box = tk.Text(root, height=12, width=80)
text_box.pack(padx=10, pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
