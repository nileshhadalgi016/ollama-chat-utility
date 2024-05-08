import streamlit as st
import psutil 
import pandas as pd
import time
import plotly.graph_objects as go

# Streamlit app
st.title("Real-time System Monitor")
st.write("Updated every 2 seconds")

# Function to display system usage
def display_usage(result):
    st.write(f"CPU Usage (%): {result['CPU Usage (%)']}")
    st.write(f"Used Cores: {result['Used Cores']}")
    st.write(f"Memory Usage (GB): {result['Memory Usage (GB)']:.2f} GB")
    st.write(f"Memory Usage (%): {result['Memory Usage (%)']}%")

# Function to collect system information
def check_system_conditions():
    # Get CPU usage for each core
    cpu_percent = psutil.cpu_percent()
    cpu_percent_per_core = psutil.cpu_percent(percpu=True)
    used_cores = sum(1 for percent in cpu_percent_per_core if percent > 0)

    # Get memory information
    memory_info = psutil.virtual_memory()
    memory_used_gb = memory_info.used / (1024 ** 3)  # Convert bytes to GB
    memory_percent = memory_info.percent

    # Collect data in a dictionary
    result = {
        'CPU Usage (%)': cpu_percent,
        'Used Cores': used_cores,
        'Memory Usage (GB)': memory_used_gb,
        'Memory Usage (%)': memory_percent
    }

    # Print the information
    print(f"System Conditions:\n"
          f"  CPU Usage (%): {result['CPU Usage (%)']} |"
          f"  Used Cores: {result['Used Cores']} |"
          f"  Memory Usage (GB): {result['Memory Usage (GB)']:.2f} GB |"
          f"  Memory Usage (%): {result['Memory Usage (%)']}%"
    )

    return result

# Create an empty dataframe to store the results
df = pd.DataFrame(columns=['Time', 'CPU Usage (%)', 'Used Cores', 'Memory Usage (GB)', 'Memory Usage (%)'])

# Function to update the dataframe and plot
def update_plot():
    fig = go.Figure()
    
    while True:
        # Get system conditions
        result = check_system_conditions()
        
        # Append current time and system conditions to the dataframe
        df.loc[len(df)] = [pd.Timestamp.now(), 
                           result['CPU Usage (%)'],
                           result['Used Cores'],
                           result['Memory Usage (GB)'],
                           result['Memory Usage (%)']]
        
        # Display the current system conditions
        display_usage(result)
        
        # Update plot
        fig.add_trace(go.Scatter(x=df['Time'], y=df['CPU Usage (%)'], name='CPU Usage (%)'))
        fig.add_trace(go.Scatter(x=df['Time'], y=df['Memory Usage (%)'], name='Memory Usage (%)'))
        
        # Update every 2 seconds
        time.sleep(2)
        st.plotly_chart(fig, use_container_width=True)

# Call the function to update the plot
update_plot()

# Once Streamlit reaches this line, it will not execute the rest of the script.
# It will continuously update the UI using the functions above.
# The script will run indefinitely until manually stopped.
