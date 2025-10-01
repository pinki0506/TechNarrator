import pandas as pd
import os

# ----------------- Part 1: Process AWT CSV -----------------
awt_file_path = r"C:\Users\ps186070\TechNarrator\AWT.csv"
awt_output_path = r"C:\Users\ps186070\TechNarrator\AWT_Processed.csv"  # Save output

def assess_health_99pct(value):
    try:
        value = float(str(value).replace('%','').strip())
    except (ValueError, TypeError):
        return "N/A or Invalid Value"

    if value < 10:
        return "Good"
    elif 10 <= value < 15:
        return "Average"
    elif 15 <= value < 20:
        return "Degraded"
    elif value >= 20:
        return "Critical"

def assess_health_100pct(value):
    try:
        value = float(str(value).replace('%','').strip())
    except (ValueError, TypeError):
        return "N/A or Invalid Value"

    if 0 < value < 5:
        return "Average"
    elif 5 <= value < 10:
        return "Degraded"
    elif value >= 10:
        return "Critical"
    else:
        return "Good"

def get_worst_health(status1, status2):
    severity_order = {"Good":1, "Average":2, "Degraded":3, "Critical":4, "N/A or Invalid Value":0}
    return status1 if severity_order.get(status1,0) >= severity_order.get(status2,0) else status2

# Load AWT CSV
if os.path.exists(awt_file_path):
    df_awt = pd.read_csv(awt_file_path)
    project_column = 'ProjectName'  # Update if needed
    awt_99_column = 'AWT86_99Pct'
    awt_100_column = 'AWT_100Pct'

    # Clean numeric columns
    df_awt[awt_99_column] = pd.to_numeric(df_awt[awt_99_column].astype(str).str.replace('%','').str.strip(), errors='coerce')
    df_awt[awt_100_column] = pd.to_numeric(df_awt[awt_100_column].astype(str).str.replace('%','').str.strip(), errors='coerce')

    # Apply health assessment
    df_awt['Health_Status'] = df_awt[awt_99_column].apply(assess_health_99pct)
    df_awt['Health_Status_B'] = df_awt[awt_100_column].apply(assess_health_100pct)

    # Final health column
    df_awt['AWT_Final_Health_Status'] = df_awt.apply(lambda row: get_worst_health(row['Health_Status'], row['Health_Status_B']), axis=1)

    # Save output
    df_awt[[project_column, 'AWT_Final_Health_Status']].to_csv(awt_output_path, index=False)
    print(f"AWT CSV processed and saved at {awt_output_path}")
else:
    print(f"AWT CSV not found at {awt_file_path}")



# ----------------- FlowControl CSV -----------------
flow_file_path = r"C:\Users\ps186070\TechNarrator\FlowControl.csv"
flow_output_path = r"C:\Users\ps186070\TechNarrator\FlowControl_Processed.csv"

# Column names mapping
project_column = 'ProjectName'
col_d = 'FCTime_30_60_secs'
col_e = 'FCTime_1_3_mins'
col_f = 'FCTime_3_5_mins'
col_g = 'FCTime_5_mins_plus'

# FlowControl health assessment functions
def assess_col_d(value):
    try: value = float(str(value).strip())
    except: return "N/A"
    if value < 10: return "Good"
    elif 10 <= value < 15: return "Average"
    elif 15 <= value < 20: return "Degraded"
    elif value >= 20: return "Critical"

def assess_col_e(value):
    try: value = float(str(value).strip())
    except: return "N/A"
    if value < 15: return "Average"
    elif 15 <= value < 20: return "Degraded"
    elif value >= 20: return "Critical"

def assess_col_f(value):
    try: value = float(str(value).strip())
    except: return "N/A"
    if value < 20: return "Degraded"
    elif value > 25: return "Critical"

def assess_col_g(value):
    try: value = float(str(value).strip())
    except: return "N/A"
    if value < 10: return "Degraded"
    elif value > 10: return "Critical"

# Function to get highest severity among multiple health statuses
def get_worst_health(status_list):
    severity_order = {"Good":1, "Average":2, "Degraded":3, "Critical":4, "N/A":0}
    worst = max(status_list, key=lambda x: severity_order.get(x,0))
    return worst

# Load FlowControl CSV
if os.path.exists(flow_file_path):
    df_flow = pd.read_csv(flow_file_path)
    df_flow.columns = df_flow.columns.str.strip()  # Remove extra spaces

    # Apply health assessments
    df_flow['Health_Col_D'] = df_flow[col_d].apply(assess_col_d)
    df_flow['Health_Col_E'] = df_flow[col_e].apply(assess_col_e)
    df_flow['Health_Col_F'] = df_flow[col_f].apply(assess_col_f)
    df_flow['Health_Col_G'] = df_flow[col_g].apply(assess_col_g)

    # Compute final health status across all four columns
    df_flow['FLOW_Final_Health_Status'] = df_flow[['Health_Col_D','Health_Col_E','Health_Col_F','Health_Col_G']].apply(lambda row: get_worst_health(row), axis=1)

    # Keep ProjectName + calculated health columns + final status
    df_output = df_flow[[project_column, 'Health_Col_D', 'Health_Col_E', 'Health_Col_F', 'Health_Col_G', 'FLOW_Final_Health_Status']]

    # Save processed output
    df_output.to_csv(flow_output_path, index=False)
    print(f"FlowControl processed health columns with final status saved at {flow_output_path}")

else:
    print(f"FlowControl CSV not found at {flow_file_path}")


# ----------------- Delay CSV -----------------
import pandas as pd
import os

# ----------------- Delay CSV -----------------
delay_file_path = r"C:\Users\ps186070\TechNarrator\Delay.csv"
delay_output_path = r"C:\Users\ps186070\TechNarrator\Delay_Processed.csv"

# Column names mapping
project_column = 'ProjectName'  # Update if different
col_c = 'Delay_1_5_min'
col_d = 'Delay_5_10_min'
col_e = 'Delay_10_30_min'
col_f = 'Delay_30_60_min'
col_g = 'Delay_60_min_plus'

# Delay health assessment functions
def assess_col_c(value):
    try:
        value = float(str(value).strip())
    except:
        return "N/A"
    if value < 1000:
        return "Good"
    elif 1000 <= value < 1500:
        return "Average"
    elif 1500 <= value < 2500:
        return "Degraded"
    elif value >= 2500:
        return "Critical"

def assess_col_d(value):
    try:
        value = float(str(value).strip())
    except:
        return "N/A"
    if value < 100:
        return "Good"
    elif 100 <= value < 200:
        return "Average"
    elif 200 <= value < 500:
        return "Degraded"
    elif value >= 500:
        return "Critical"

def assess_col_e(value):
    try:
        value = float(str(value).strip())
    except:
        return "N/A"
    if 50 <= value < 100:
        return "Average"
    elif 100 <= value < 200:
        return "Degraded"
    elif value >= 200:
        return "Critical"
    else:
        return "Good"

def assess_col_f(value):
    try:
        value = float(str(value).strip())
    except:
        return "N/A"
    if 20 <= value < 50:
        return "Average"
    elif 50 <= value < 100:
        return "Degraded"
    elif value >= 100:
        return "Critical"
    else:
        return "Good"

def assess_col_g(value):
    try:
        value = float(str(value).strip())
    except:
        return "N/A"
    if value < 10:
        return "Average"
    elif value >= 10:
        return "Critical"
    else:
        return "N/A"

# Function to get highest severity among multiple health statuses
def get_worst_health(status_list):
    severity_order = {"Good":1, "Average":2, "Degraded":3, "Critical":4, "N/A":0}
    worst = max(status_list, key=lambda x: severity_order.get(x, 0))
    return worst

# Load Delay CSV
if os.path.exists(delay_file_path):
    df_delay = pd.read_csv(delay_file_path)
    df_delay.columns = df_delay.columns.str.strip()  # Remove extra spaces

    # Apply health assessments
    df_delay['Health_Col_C'] = df_delay[col_c].apply(assess_col_c)
    df_delay['Health_Col_D'] = df_delay[col_d].apply(assess_col_d)
    df_delay['Health_Col_E'] = df_delay[col_e].apply(assess_col_e)
    df_delay['Health_Col_F'] = df_delay[col_f].apply(assess_col_f)
    df_delay['Health_Col_G'] = df_delay[col_g].apply(assess_col_g)

    # Compute final health status across all five columns
    df_delay['Delay_Final_Health_Status'] = df_delay[
        ['Health_Col_C','Health_Col_D','Health_Col_E','Health_Col_F','Health_Col_G']
    ].apply(lambda row: get_worst_health(row), axis=1)

    # Keep only ProjectName, calculated health columns, and final status
    df_output = df_delay[
        [project_column, 'Health_Col_C','Health_Col_D','Health_Col_E','Health_Col_F','Health_Col_G','Delay_Final_Health_Status']
    ]

    # Save processed output
    df_output.to_csv(delay_output_path, index=False)
    print(f"Delay CSV processed and saved at {delay_output_path}")

else:
    print(f"Delay CSV not found at {delay_file_path}")

# ----------------- File Paths -----------------
awt_processed_path = r"C:\Users\ps186070\TechNarrator\AWT_Processed.csv"
flow_processed_path = r"C:\Users\ps186070\TechNarrator\FlowControl_Processed.csv"
delay_processed_path = r"C:\Users\ps186070\TechNarrator\Delay_Processed.csv"
final_output_path = r"C:\Users\ps186070\TechNarrator\Consolidated_Final_Health.csv"

# Load processed CSVs
df_awt = pd.read_csv(awt_processed_path)
df_flow = pd.read_csv(flow_processed_path)
df_delay = pd.read_csv(delay_processed_path)

# Strip column names to remove extra spaces
df_awt.columns = df_awt.columns.str.strip()
df_flow.columns = df_flow.columns.str.strip()
df_delay.columns = df_delay.columns.str.strip()

# Merge on ProjectName safely
df_merged = pd.merge(df_awt, df_flow, on='ProjectName', how='outer')
df_merged = pd.merge(df_merged, df_delay, on='ProjectName', how='outer')

# Keep only ProjectName + final health columns
df_final = df_merged[['ProjectName', 'AWT_Final_Health_Status', 'FLOW_Final_Health_Status', 'Delay_Final_Health_Status']]

# Save final consolidated CSV
df_final.to_csv(final_output_path, index=False)
print(f"Consolidated final health CSV saved at {final_output_path}")

# Print the final output
print("\n--- Consolidated Final Health Status ---")
print(df_final)
