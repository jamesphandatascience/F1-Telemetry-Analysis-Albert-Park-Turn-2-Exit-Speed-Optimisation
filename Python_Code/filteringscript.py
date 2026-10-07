import Filtering as fil
import pandas as pd

if __name__ == "__main__":
    #Load the raw data
    f12024 = pd.read_csv("UNSW F12024.csv")
    left = pd.read_csv('f1sim-ref-left.csv')
    right = pd.read_csv('f1sim-ref-right.csv')
    line = pd.read_csv('f1sim-ref-line.csv')
    turns = pd.read_csv('f1sim-ref-turns.csv')

    # Filter
    df = f12024.copy()
    print(f"Initial dataset shape: {df.shape}")

    # Step 1: Filter track section
    print("\n[1/6] Filtering track section...")
    df, left, right, line, turns = fil.filter_track_section(df, left, right, line, turns)
    print(f"After filter_track_section → Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    # Step 2: Keep relevant features
    print("\n[2/6] Keeping relevant features...")
    df = fil.keep_relevant_features(df)
    print(f"After keep_relevant_features → Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    # Step 3: Remove NaN values
    print("\n[3/6] Removing NaN values...")
    df = fil.remove_nan(df)
    print(f"After remove_nan → Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    # Step 4: Remove non-driving behaviour
    print("\n[4/6] Removing non-driving behaviour...")
    df = fil.remove_nondriving_behaviour(df)
    print(f"After remove_nondriving_behaviour → Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    # Step 5: Deduplicate XYZ positions
    print("\n[5/6] Deduplicating XYZ positions...")
    df = fil.dedupe_xyz(df)
    print(f"After dedupe_xyz → Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    # Step 6: Remove incomplete laps
    print("\n[6/6] Removing incomplete laps...")
    df = fil.remove_incomplete_laps(df)
    print(f"After remove_incomplete_laps → Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    print("\n✅ Filtering complete!")
    print(f"Final dataset shape: {df.shape}")

    df.to_csv("UNSW_F12024_cleaned.csv", index=False)
    left.to_csv('f1sim-ref-left_cleaned.csv', index=False)
    right.to_csv('f1sim-ref-right_cleaned.csv', index=False)
    line.to_csv('f1sim-ref-line_cleaned.csv', index=False)
    turns.to_csv('f1sim-ref-turns_cleaned.csv', index=False)