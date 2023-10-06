import fastf1
import fastf1.plotting
import numpy as np
from matplotlib import pyplot as plt

fastf1.Cache.enable_cache('Cache')

# The misc_mpl_mods option enables minor grid lines which clutter the plot
fastf1.plotting.setup_mpl(misc_mpl_mods=False)

session = fastf1.get_session(2023, "British Grand Prix", 'R')
session.load()
session_name = "R"

def plot_trackTemp_and_airTemp(session, session_name):
    session.weather_data.columns
    y1 = session.weather_data.AirTemp
    y2 = session.weather_data.TrackTemp
    x = session.weather_data.Time
    # Creating figure
    fig = plt.figure()
    
    # Plotting dataset_2
    ax = fig.add_subplot(111)
    ax.plot(x, y1, '-', label='AirTemp')
    
    # Creating Twin axes for dataset_1
    ax2 = ax.twinx()
    ax2.plot(x, y2, '-r', label='TrackTemp')
    
    # Adding legend
    ax.legend(loc=2)
    ax2.legend(loc=0)

    ax2.set_yticks(np.linspace(ax2.get_yticks()[0], ax2.get_yticks()[-1], len(ax.get_yticks())))
    
    # adding grid
    ax.grid(color="pink", linestyle="-")
    ax2.grid(color="r", linestyle=":")
    
    # Adding labels
    ax.set_xlabel("Time")
    ax.set_ylabel(r"AirTemp")
    ax2.set_ylabel(r"TrackTemp")
    
    # Show plot
    plt.suptitle(f"AirTemp and TrackTemp \n "f"{session.event['EventName']} {session.event.year} {session_name}")
    plt.figure().set_size_inches(50000, 500000, forward=True)
    plt.show()

plot_trackTemp_and_airTemp(session, "R")