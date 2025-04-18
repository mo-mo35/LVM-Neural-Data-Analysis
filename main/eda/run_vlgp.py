#run_vlgp.py
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from src import analysis
import pickle

# --- Load configuration ---
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)
BIN_SIZE = config["bin_size"]
PRE_TIME = config["pre_time"]
POST_TIME = config["post_time"]
forced_session_id = "ca5404f7-297c-40f1-bbf0-5ac0a63e24f8" # "11a5a93e-58a9-4ed0-995e-52279ec16b98"
def main():
    # Run session search by region.
    print("Running session search by region...")
    region_sessions, common_sessions = analysis.search_sessions_by_region()
    
    # Report total sessions.
    all_sessions = set()
    for sessions in region_sessions.values():
        all_sessions.update(sessions)
    print(f"\nTotal unique sessions found (union): {len(all_sessions)}")
    for s in all_sessions:
        print(f"  {s}")
    
    # Select sessions with diverse region combinations.
    diverse_sessions = analysis.select_diverse_sessions(region_sessions, common_sessions, max_sessions=50)
    print(f"\nRunning full analysis on a subset of {len(diverse_sessions)} diverse sessions...")
    
     # Run full analysis to obtain sensitive clusters per session/event type.
    sensitive_clusters = analysis.run_full_analysis(diverse_sessions, force_session = forced_session_id)
    filtered_sensitive_clusters = analysis.filter_sensitive_clusters(sensitive_clusters, top_n_regions=2)

    # Group sensitive clusters by region for each event type and fit vLGP models.
    fitted_models = analysis.fit_vlgp_models_by_region(filtered_sensitive_clusters, force_session = forced_session_id)
    
    # Print summary of fitted models.
    for session, event_dict in fitted_models.items():
        for event_type, region_dict in event_dict.items():
            for region, model in region_dict.items():
                print(f"Session {session} | Event {event_type} | Region {region} fitted model with {len(model['trials'])} trials.")
    
if __name__ == "__main__":
    main()
