import os
import pandas as pd
import numpy as np
import Functions as f  # assumes your utilities live in Functions.py

if __name__ == "__main__":
    # ---- Config: where to save ----
    target_dir = "."  # change to "Data/Engineered_Data" if you want a subfolder
    os.makedirs(target_dir, exist_ok=True)

    # ---- Load cleaned lap data ----
    df = pd.read_csv("UNSW_F12024_cleaned.csv")

    # ---- Load reference geometry (needed for normal & barrier lookups) ----
    left  = pd.read_csv("f1sim-ref-left_cleaned.csv")
    right = pd.read_csv("f1sim-ref-right_cleaned.csv")

    # ---- Define critical points ----
    turn2x, turn2y = 368.93, 90.000
    turn1x, turn1y = 375.57, 191.519
    brakex, brakey = 343.2, 244.4
    midx, midy     = (turn2x + turn1x) / 2 - 6.7, (turn2y + turn1y) / 2

    # ---- Helper to build & save one dataset ----
    def build_and_save(name: str, x0: float, y0: float):
        print(f"\n[Build] {name} at point ({x0:.3f}, {y0:.3f}) ...")
        stats = f.build_dataset(df, left, right, x0, y0)  # uses your updated function
        out_path = os.path.join(target_dir, name)
        stats.to_csv(out_path, index=False)
        print(f"Saved: {out_path} | Rows: {len(stats)}, Cols: {stats.shape[1]}")
        return stats

    # ---- Produce all engineered datasets ----
    turn_2_stats       = build_and_save("turn_2_stats.csv",       turn2x, turn2y)
    turn_1_stats       = build_and_save("turn_1_stats.csv",       turn1x, turn1y)
    brake_point_stats  = build_and_save("brake_point_stats.csv",  brakex, brakey)
    mid_point_stats    = build_and_save("mid_point_stats.csv",    midx,   midy)

    print("\n✅ All engineered datasets generated.")
    