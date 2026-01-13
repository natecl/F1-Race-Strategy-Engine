import fastf1
import pandas as pd

#Set up the cache to reduce fetching time
fastf1.Cache.enable_cache("cache/")

#Creates the session object for the 2023 Monza Grand Prix Race data and loads it
session = fastf1.get_session(2023, "Monza", "R")
session.load()

#Make a copy of the raw lap data
laps_raw = session.laps.copy()

'''
prints the number of laps that are inaccurate and the titles for all laps
print(len(laps_raw), "rows")
print(laps_raw.columns)
'''

#cleans the data by removing inaccurate, deleted, and incomplete laps
laps_clean = laps_raw [
    (laps_raw["IsAccurate"] == True) &
    (laps_raw["Deleted"] == False) &
    (laps_raw["LapTime"].notna()) &
    (laps_raw["LapNumber"].notna()) &
    (laps_raw["Position"].notna())
].copy()

#Shows reduction of inaccurate laps
print(len(laps_raw), "->" , len(laps_clean))

#Converts all the data types to the correct ones for easier processing in LapNumber and Position
laps_clean["LapNumber"] = laps_clean["LapNumber"].astype(int)
laps_clean["Position"] = laps_clean["Position"].astype(int)

#Prints the data types of the two columns
print(laps_clean[["LapNumber", "Position"]].dtypes)

#arranges the dataframe in order of the driver then the lap numbers
laps_clean = laps_clean.sort_values( by = ["Driver", "LapNumber"] ).copy()

#creates a new column called stint_lap which counts the number of laps in a particular stint
laps_clean["Stint_lap"] = (
    laps_clean.groupby(["Driver", "Stint"])
    .cumcount() + 1
)

#Print a Dataframe that only contains data of Verstappen and only the columns of LapNumber, Stint, and Stint_lap for the first 20 laps
print(
    laps_clean[laps_clean["Driver"] == "VER"]
    [["LapNumber", "Stint", "Stint_lap"]]
    .head(20)
)

#Create a lookup dataframe that uses a Hierarchal index with LapNumber and Position that contains data in the lap_end_time column
lookup = (
    laps_clean[["LapNumber", "Position", "Time"]]
    .rename(columns = {"Time": "lap_end_time"})
    .set_index(["LapNumber", "Position"])
)

#Creates a sample lookup for P2 at the end of lap 2
sample = lookup.loc[(2,2), "lap_end_time"]
print(sample, "lap end time for P2 on Lap 2")

#Creates a new column called ahead_position which is the position ahead of the current car
laps_clean["ahead_position"] = laps_clean["Position"] - 1

#Creates a copy of the lookup table and changes the index name to match the new column in laps_clean
lookup_ahead = lookup.copy()
lookup_ahead.index = lookup_ahead.index.set_names(
    ["LapNumber", "ahead_position"]
)

#Joins the lookup table to the laps_clean dataframe
laps_clean = laps_clean.join(
    lookup_ahead,
    on = ["LapNumber", "ahead_position"],
)

#Calculates the gap ahead of each car
laps_clean[ "gap_ahead"] = laps_clean[ "Time"] - laps_clean["lap_end_time"]

#For the cars in P1, there is no car ahead of them, so we set the gap_ahead to None for those rows
laps_clean.loc[laps_clean["Position"] == 1, "gap_ahead"] = pd.NaT

#Prints a DataFrame that only contains data of Verstappen and only the columns of LapNumber, Position, and gap_ahead for the first 20 laps
print(
    laps_clean[laps_clean["Driver"] == "VER"]
    [["LapNumber", "Position", "gap_ahead"]]
    .head(10)
)

#Selects only the data for Verstappen
driver = "VER"
laps_driver = laps_clean[laps_clean["Driver"] == driver].copy()

out = (
    laps_driver[["LapNumber", "Compound", "LapTime", "Stint_lap", "TrackStatus", "Position", "gap_ahead"]]
    .rename(columns={
         "LapNumber": "lap",
        "Compound": "compound",
        "LapTime": "lap_time",
        "TrackStatus": "track_status",
        "Position": "position",
    })
    .sort_values(by = "lap")
)

print(out.head(20).to_string(index=False))

