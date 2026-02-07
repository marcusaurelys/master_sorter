import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
from sorting import (
    bubble_sort, insertion_sort, selection_sort,
    shell_insertion_logic, shell_bubble_logic, get_gaps
)

st.set_page_config(page_title="Algorithm Growth Rate Analyzer", layout="wide")

st.title("📊 Sorting Visualization & Growth Analysis")

# --- SIDEBAR: DATA INPUT ---
st.sidebar.header("1. Data Input Configuration")
input_option = st.sidebar.radio("Choose Input Method:", ["Data Generator", "Custom Input"])

data_to_sort = []
intervals = 5

if input_option == "Data Generator":
    max_N = st.sidebar.number_input("max_N (Number of points)", value=100, min_value=10)
    n_intervals = st.sidebar.number_input("N_intervals", value=5, min_value=2)
    max_val = st.sidebar.number_input("max_n (Highest value)", value=100)
    low_val = st.sidebar.number_input("low_n (Lowest value)", value=1)
    
    dist_type = st.sidebar.selectbox("Distribution", ["Sequence/Uniform", "Normal Distribution"])
    nature = st.sidebar.selectbox("Nature of Data", ["Random", "Almost Sorted", "Reversed"])
    
    if dist_type == "Normal Distribution":
        data_to_sort = np.random.normal(loc=(max_val+low_val)/2, scale=(max_val-low_val)/6, size=max_N).tolist()
    else:
        # Sequence logic: (low_n, low_n + step, ..., max_n)
        step_val = (max_val - low_val) / max_N
        data_to_sort = [low_val + i * step_val for i in range(max_N)]
        
        if nature == "Random":
            np.random.shuffle(data_to_sort)
        elif nature == "Almost Sorted":
            data_to_sort.sort()
            if len(data_to_sort) >= 2:
                data_to_sort[0], data_to_sort[-1] = data_to_sort[-1], data_to_sort[0]
        elif nature == "Reversed":
            data_to_sort.sort(reverse=True)
    
    intervals = n_intervals

else:
    raw_input = st.sidebar.text_area("Paste data (comma or space separated)")
    data_type = st.sidebar.selectbox("Sort as:", ["Numbers", "Strings"])
    n_intervals = st.sidebar.number_input("N_intervals", value=5, min_value=2)
    
    if raw_input:
        import re
        parsed = re.split(r'[,\s]+', raw_input.strip())
        if data_type == "Numbers":
            data_to_sort = [float(x) for x in parsed if x]
        else:
            data_to_sort = [str(x) for x in parsed if x]
    
    max_N = len(data_to_sort)
    intervals = n_intervals

# --- ALGORITHM SELECTION ---
st.sidebar.header("2. Algorithm Selection")
algos = st.sidebar.multiselect("Select Algorithms:", [
    "Bubble Sort", "Insertion Sort", "Selection Sort",
    "Shell Sort (N/2^k)", "Shell Bubble Sort (N/2^k)",
    "Shell Sort (Hibbard)", "Shell Bubble Sort (Hibbard)",
    "Shell Sort (Knuth)", "Shell Insertion Sort (Knuth)",
    "Custom Shell Sort", "Custom Shell Bubble Sort"
])

custom_gaps_input = []
if "Custom Shell Sort" in algos or "Custom Shell Bubble Sort" in algos:
    g_str = st.sidebar.text_input("Custom Gaps (e.g. 5, 3, 1)", "5, 2, 1")
    custom_gaps_input = [int(x.strip()) for x in g_str.split(",") if x.strip()]

do_viz = st.sidebar.checkbox("Show Live Visualization? (not recommended for large inputs)", value=False)

# --- EXECUTION ENGINE ---
if st.button("🚀 Run Analysis"):
    if not algos or not data_to_sort:
        st.warning("Please select algorithms and provide data.")
    else:
        # Prep results storage
        comparison_results = []
        swap_results = []
        
        # Step calculation
        step_size = max(1, max_N // intervals)
        n_sizes = [step_size * i for i in range(1, intervals + 1)]
        if n_sizes[-1] < max_N: n_sizes.append(max_N)

        for algo_name in algos:
            algo_comparisons = {"Algorithm": algo_name}
            algo_swaps = {"Algorithm": algo_name}
            
            for N in n_sizes:
                subset = data_to_sort[:N].copy()
                count = {"comparisons": 0, "swaps": 0}
                
                # Logic Switcher
                if algo_name == "Bubble Sort":
                    list(bubble_sort(subset, count))
                elif algo_name == "Insertion Sort":
                    list(insertion_sort(subset, count))
                elif algo_name == "Selection Sort":
                    list(selection_sort(subset, count))
                elif "Shell" in algo_name:
                    # Determine gap sequence
                    if "Hibbard" in algo_name: method = "hibbard"
                    elif "Knuth" in algo_name: method = "knuth"
                    elif "Custom" in algo_name: method = "custom"
                    else: method = "shell"
                    
                    gaps = get_gaps(N, method, custom_gaps_input)
                    
                    if "Bubble" in algo_name:
                        list(shell_bubble_logic(subset, count, gaps))
                    else:
                        list(shell_insertion_logic(subset, count, gaps))
                
                algo_comparisons[f"N={N}"] = count["comparisons"]
                algo_swaps[f"N={N}"] = count["swaps"]
            
            comparison_results.append(algo_comparisons)
            swap_results.append(algo_swaps)

        # --- VISUALIZATION (Animation) ---
        if do_viz:
            st.subheader("Live Visualization")
            viz_cols = st.columns(len(algos))
            for idx, algo_name in enumerate(algos):
                with viz_cols[idx]:
                    st.caption(algo_name)
                    chart_placeholder = st.empty()
                    subset = data_to_sort[:max_N].copy()
                    count = {"comparisons": 0, "swaps": 0}
                    
                    # Generators for animation
                    gen = None
                    if algo_name == "Bubble Sort": gen = bubble_sort(subset, count, True)
                    elif algo_name == "Insertion Sort": gen = insertion_sort(subset, count, True)
                    elif algo_name == "Selection Sort": gen = selection_sort(subset, count, True)
                    elif "Shell" in algo_name:
                        m = "hibbard" if "Hibbard" in algo_name else "knuth" if "Knuth" in algo_name else "custom" if "Custom" in algo_name else "shell"
                        gs = get_gaps(max_N, m, custom_gaps_input)
                        if "Bubble" in algo_name: gen = shell_bubble_logic(subset, count, gs, True)
                        else: gen = shell_insertion_logic(subset, count, gs, True)
                    
                    if gen:
                        for state in gen:
                            chart_placeholder.bar_chart(state)

        # --- GROWTH RATE GRAPHS ---
        st.divider()
        df_comp = pd.DataFrame(comparison_results)
        df_swap = pd.DataFrame(swap_results)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Growth Rate: Comparisons")
            # Melt dataframe for Plotly
            df_comp_melted = df_comp.melt(id_vars=["Algorithm"], var_name="N", value_name="Count")
            df_comp_melted["N"] = df_comp_melted["N"].str.replace("N=", "").astype(int)
            fig1 = px.line(df_comp_melted, x="N", y="Count", color="Algorithm", markers=True)
            st.plotly_chart(fig1, use_container_width=True)
            st.download_button("Download Comparisons CSV", df_comp.to_csv(index=False), "comparisons.csv")

        with col2:
            st.subheader("Growth Rate: Swaps")
            df_swap_melted = df_swap.melt(id_vars=["Algorithm"], var_name="N", value_name="Count")
            df_swap_melted["N"] = df_swap_melted["N"].str.replace("N=", "").astype(int)
            fig2 = px.line(df_swap_melted, x="N", y="Count", color="Algorithm", markers=True)
            st.plotly_chart(fig2, use_container_width=True)
            st.download_button("Download Swaps CSV", df_swap.to_csv(index=False), "swaps.csv")