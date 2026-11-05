from f1_common import enable_cache

import fastf1
import fastf1.plotting
from matplotlib import pyplot as plt


enable_cache()

session = fastf1.get_session(2023, "British Grand Prix", 'R')
session.load()
laps = session.laps

drivers = session.drivers
print(drivers)


drivers = [session.get_driver(driver)["Abbreviation"] for driver in drivers]
print(drivers)

stints = laps[["Driver", "Stint", "Compound", "LapNumber"]]
stints = stints.groupby(["Driver", "Stint", "Compound"])
stints = stints.count().reset_index()

stints = stints.rename(columns={"LapNumber": "StintLength"})
print(stints)

fig, ax = plt.subplots(figsize=(5, 10))

for driver in drivers:
    driver_stints = stints.loc[stints["Driver"] == driver]

    previous_stint_end = 0
    for idx, row in driver_stints.iterrows():
        plt.barh(
            y=driver,
            width=row["StintLength"],
            left=previous_stint_end,
            color=fastf1.plotting.get_compound_color(row["Compound"], session),
            edgecolor="black",
            fill=True
        )

        previous_stint_end += row["StintLength"]

plt.title("2023 British Grand Prix Strategies")
plt.xlabel("Lap Number")
plt.grid(False)
ax.invert_yaxis()

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.tight_layout()
plt.show()
