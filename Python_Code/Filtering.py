import numpy as np

# Remove rows with nan in important feature columns
# E.g Usage: df = remove_nan(df)
def remove_nan(df):
    
    value = ['SESSION_GUID','M_SPEED_1', 'M_THROTTLE_1', 'M_STEER_1', 'M_BRAKE_1', 'M_GEAR_1']
    
    # NAN for inf values
    df = df.replace([np.inf, -np.inf], np.nan)
    
    # drop rows with nan values in the specified columns
    cleaned = df.dropna(subset = value)
    
    return cleaned


# Filter telemetry and reference data to specific section of the Albeit Park Track
# E.g Usage: df, left, right, line, turns = filter_track_section(df, left, right, line, turns)
def filter_track_section(df, left, right, line, turns, 
                         track_id=0, sector_id=0, 
                         xl=200, xr=600, yd=-180, yu=400):

    # Filter telemetry
    df_filtered = df[(df["M_TRACKID"] == track_id) & (df["M_SECTOR_1"] == sector_id)]
    df_filtered = df_filtered[
        (df_filtered["M_WORLDPOSITIONX_1"].between(xl, xr)) &
        (df_filtered["M_WORLDPOSITIONY_1"].between(yd, yu))
    ]

    # Filter boundaries
    def filter_bounds(df_ref):
        return df_ref[
            (df_ref["WORLDPOSX"].between(xl, xr)) &
            (df_ref["WORLDPOSY"].between(yd, yu))
        ]

    left_filtered  = filter_bounds(left)
    right_filtered = filter_bounds(right)
    line_filtered  = filter_bounds(line)

    # Filter turns (keep only turns 1 and 2)
    turns_filtered = turns[turns["TURN"].isin([1, 2])]

    return df_filtered, left_filtered, right_filtered, line_filtered, turns_filtered

import pandas as pd

# Keep only the relevant features for the Turn 2 exit speed research
# df = keep_relevant_features(df)
def keep_relevant_features(df):
    relevant_columns = [
        "SESSION_GUID",
        "M_TIMESTAMP",
        "M_CURRENTLAPNUM",
        "M_SPEED_1",
        "M_THROTTLE_1",
        "M_STEER_1",
        "M_BRAKE_1",
        "M_GEAR_1",
        "M_CURRENTLAPINVALID_1",
        "M_WORLDPOSITIONX_1",
        "M_WORLDPOSITIONY_1",
        "M_WORLDPOSITIONZ_1"
    ]

    # Filter and return
    return df[relevant_columns].copy()

# Remove laps that contain reverse, neutral, or slow-speed behavior within a specific section of the track.
# E.g usage: df = remove_nondriving_behaviour(df)
def remove_nondriving_behaviour(df, x_range=(300, 400), y_range=(80, 250), speed_threshold=40):

    # Filter to the section of interest
    section_df = df[
        (df["M_WORLDPOSITIONX_1"].between(x_range[0], x_range[1])) &
        (df["M_WORLDPOSITIONY_1"].between(y_range[0], y_range[1]))
    ].copy()

    # Identify laps that have reverse, neutral, or too slow speed
    bad_laps = section_df[
        (section_df["M_GEAR_1"] <= 0) | (section_df["M_SPEED_1"] < speed_threshold)
    ][["SESSION_GUID", "M_CURRENTLAPNUM"]].drop_duplicates()

    # Filter out those laps from the full dataset
    filtered_df = df.merge(bad_laps, on=["SESSION_GUID", "M_CURRENTLAPNUM"], how="left", indicator=True)
    filtered_df = filtered_df[filtered_df["_merge"] == "left_only"].drop(columns="_merge")

    return filtered_df

# Removes repeating xyz coordinates (stagnant positions) and leaves first instance
# E.g usage: df = dedupe_xyz(df)
def dedupe_xyz(
    df,
    group_cols=("SESSION_GUID", "M_CURRENTLAPNUM"),
    pos_cols=("M_WORLDPOSITIONX_1", "M_WORLDPOSITIONY_1", "M_WORLDPOSITIONZ_1"),
    keep="first"
):
    df2 = df.copy()
    subset = list(group_cols) + list(pos_cols)
    out = df2.drop_duplicates(subset=subset, keep=keep)
    
    return out

# Remove laps with abnormal (too few or too many) data points within a section of the track
# E.g usage: df = remove_incomplete_laps(df)
def remove_incomplete_laps(df, x_range=(300, 400), y_range=(70, 250), lower_bound=180, upper_bound=220):

    # Filter to section of track
    section = df[
        (df["M_WORLDPOSITIONX_1"].between(x_range[0], x_range[1])) &
        (df["M_WORLDPOSITIONY_1"].between(y_range[0], y_range[1]))
    ].copy()

    # Compute counts per (session, lap)
    lap_counts = (
        section.groupby(["SESSION_GUID", "M_CURRENTLAPNUM"])
        .size()
        .reset_index(name="row_count")
    )

    # Identify complete laps
    complete_laps = lap_counts[lap_counts["row_count"].between(lower_bound, upper_bound)]

    # Keep only complete laps in original dataframe
    filtered_df = df.merge(
        complete_laps[["SESSION_GUID", "M_CURRENTLAPNUM"]],
        on=["SESSION_GUID", "M_CURRENTLAPNUM"],
        how="inner"
    )

    return filtered_df








