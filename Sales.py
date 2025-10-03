import pandas as pd
import os

# ----------------- Setup -----------------
BASE_DIR = r"C:\Users\ps186070\TechNarrator"
OUTPUT_DIR = os.path.join(BASE_DIR, "Output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_output(df, filename, cols=None):
    """Helper to save processed DataFrame into Output folder"""
    path = os.path.join(OUTPUT_DIR, filename)
    if cols:
        df = df[cols]
    df.to_csv(path, index=False)
    print(f"Saved: {path}")
    return path

# Severity mapping (reused everywhere)
SEVERITY_ORDER = {"Good":1, "Average":2, "Degraded":3, "Critical":4, "N/A":0, "N/A or Invalid Value":0}

def worst_status(status_list):
    return max(status_list, key=lambda x: SEVERITY_ORDER.get(x, 0))


# ----------------- Part 1: AWT -----------------
awt_file = os.path.join(BASE_DIR, "AWT.csv")

def assess_99(value):
    try: v = float(str(value).replace('%','').strip())
    except: return "N/A or Invalid Value"
    return "Good" if v < 10 else "Average" if v < 15 else "Degraded" if v < 20 else "Critical"

def assess_100(value):
    try: v = float(str(value).replace('%','').strip())
    except: return "N/A or Invalid Value"
    if 0 < v < 5: return "Average"
    elif v < 10: return "Degraded" if v >= 5 else "Good"
    return "Critical" if v >= 10 else "Good"

if os.path.exists(awt_file):
    df_awt = pd.read_csv(awt_file)
    df_awt.columns = df_awt.columns.str.strip()
    df_awt['Health_99'] = df_awt['AWT86_99Pct'].apply(assess_99)
    df_awt['Health_100'] = df_awt['AWT_100Pct'].apply(assess_100)
    df_awt['AWT_Final_Health_Status'] = df_awt.apply(
        lambda r: worst_status([r['Health_99'], r['Health_100']]), axis=1
    )
    awt_out = save_output(df_awt, "AWT_Processed.csv", ['ProjectName', 'AWT_Final_Health_Status'])
else:
    print(f"AWT file missing: {awt_file}")


# ----------------- Part 2: FlowControl -----------------
flow_file = os.path.join(BASE_DIR, "FlowControl.csv")

def assess(value, thresholds):
    try: v = float(str(value).strip())
    except: return "N/A"
    for limit, label in thresholds:
        if v < limit: return label
    return thresholds[-1][1]  # fallback highest severity

if os.path.exists(flow_file):
    df_flow = pd.read_csv(flow_file)
    df_flow.columns = df_flow.columns.str.strip()

    df_flow['Health_D'] = df_flow['FCTime_30_60_secs'].apply(lambda x: assess(x, [(10,"Good"),(15,"Average"),(20,"Degraded"),(99999,"Critical")]))
    df_flow['Health_E'] = df_flow['FCTime_1_3_mins'].apply(lambda x: assess(x, [(15,"Average"),(20,"Degraded"),(99999,"Critical")]))
    df_flow['Health_F'] = df_flow['FCTime_3_5_mins'].apply(lambda x: assess(x, [(20,"Degraded"),(25,"Degraded"),(99999,"Critical")]))
    df_flow['Health_G'] = df_flow['FCTime_5_mins_plus'].apply(lambda x: assess(x, [(10,"Degraded"),(99999,"Critical")]))

    df_flow['FLOW_Final_Health_Status'] = df_flow[['Health_D','Health_E','Health_F','Health_G']].apply(lambda r: worst_status(r), axis=1)

    flow_out = save_output(df_flow, "FlowControl_Processed.csv", 
                           ['ProjectName','Health_D','Health_E','Health_F','Health_G','FLOW_Final_Health_Status'])
else:
    print(f"FlowControl file missing: {flow_file}")


# ----------------- Part 3: Delay -----------------
delay_file = os.path.join(BASE_DIR, "Delay.csv")

if os.path.exists(delay_file):
    df_delay = pd.read_csv(delay_file)
    df_delay.columns = df_delay.columns.str.strip()

    df_delay['Health_C'] = df_delay['Delay_1_5_min'].apply(lambda x: assess(x, [(1000,"Good"),(1500,"Average"),(2500,"Degraded"),(999999,"Critical")]))
    df_delay['Health_D'] = df_delay['Delay_5_10_min'].apply(lambda x: assess(x, [(100,"Good"),(200,"Average"),(500,"Degraded"),(999999,"Critical")]))
    df_delay['Health_E'] = df_delay['Delay_10_30_min'].apply(lambda x: assess(x, [(50,"Good"),(100,"Average"),(200,"Degraded"),(999999,"Critical")]))
    df_delay['Health_F'] = df_delay['Delay_30_60_min'].apply(lambda x: assess(x, [(20,"Good"),(50,"Average"),(100,"Degraded"),(999999,"Critical")]))
    df_delay['Health_G'] = df_delay['Delay_60_min_plus'].apply(lambda x: assess(x, [(10,"Average"),(999999,"Critical")]))

    df_delay['Delay_Final_Health_Status'] = df_delay[['Health_C','Health_D','Health_E','Health_F','Health_G']].apply(lambda r: worst_status(r), axis=1)

    delay_out = save_output(df_delay, "Delay_Processed.csv",
                            ['ProjectName','Health_C','Health_D','Health_E','Health_F','Health_G','Delay_Final_Health_Status'])
else:
    print(f"Delay file missing: {delay_file}")


# ----------------- Final Merge -----------------
try:
    df_awt = pd.read_csv(awt_out)
    df_flow = pd.read_csv(flow_out)
    df_delay = pd.read_csv(delay_out)

    df_final = df_awt.merge(df_flow, on="ProjectName", how="outer").merge(df_delay, on="ProjectName", how="outer")
    final_out = save_output(df_final, "Consolidated_Final_Health.csv",
                            ['ProjectName','AWT_Final_Health_Status','FLOW_Final_Health_Status','Delay_Final_Health_Status'])

    print("\n--- Consolidated Final Health Status ---")
    print(df_final)
except Exception as e:
    print(f"Final merge skipped due to missing processed files: {e}")
