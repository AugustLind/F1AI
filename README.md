# F1AI

Formula 1 data-analysis experiments using Python, FastF1, and Matplotlib.
Most examples visualize the 2023 British Grand Prix. A separate early LSTM
experiment explores race-position prediction; this is not a validated race
prediction system.

## Setup

Use Python 3.11 or later and a virtual environment. From the repository root:

```bash
git clone https://github.com/AugustLind/F1AI.git
cd F1AI
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the environment with `.venv\Scripts\Activate.ps1` in
PowerShell instead. Matplotlib needs a graphical backend to display windows;
headless environments require configuring a backend and saving figures instead.

The dependency file gives compatibility ranges, not an exact lockfile. FastF1
plotting calls use the session-aware API available in FastF1 3.6 and later.
See the [FastF1 plotting source/API](https://github.com/theOehrly/Fast-F1/tree/master/fastf1/plotting).

## Plotting examples

Run a script from the activated environment, for example:

```bash
python position_changes.py
```

| Script | Output |
|---|---|
| [position_changes.py](position_changes.py) | Driver position over race laps |
| [qualifying_result.py](qualifying_result.py) | Fastest qualifying lap deltas to pole |
| [race_pace.py](race_pace.py) | Team lap-time distributions after quick-lap filtering |
| [speed_traps.py](speed_traps.py) | Each team's maximum speed-trap value among its drivers' fastest laps |
| [track_temperature.py](track_temperature.py) | Track and air temperature over the session |
| [tyre_strategy.py](tyre_strategy.py) | Driver stints grouped by tyre compound |

Edit the year, Grand Prix, and session identifier inside a script to analyze
another event. `R` selects the race and `Q` qualifying. Data availability and
coverage depend on the event and upstream services; scripts may need additional
handling for incomplete sessions or drivers without a valid lap.

The original scripts without extensions and mixed-case filenames have been
renamed to the snake_case `.py` filenames listed above. `Prediction` is now
`prediction.py`, and `TrackTemprature.py` is now `track_temperature.py`.

## Data and caching

Every plotting script calls [f1_common.py](f1_common.py), which creates `Cache/`
beside the scripts before enabling FastF1 caching. The location is independent
of the shell's working directory.

On the first run, FastF1 downloads the requested session data. Later runs reuse
the local cache where possible. An internet connection is needed when requested
data is not already cached. The examples can recreate their cache from upstream
sources; generated pickle and SQLite files are not distributed in this branch.

You can delete your local `Cache/` directory while scripts are stopped to force
data to be fetched again. It can grow large, so `.gitignore` excludes it along
with Python environments, bytecode, and local environment files.

The cleanup removes previously committed caches from the current tree only.
Older commits still contain those files, so a normal clone may remain large.
Removing them from Git history would require a separate history rewrite and
coordination with existing clones. To download only the current snapshot:

```bash
git clone --depth 1 https://github.com/AugustLind/F1AI.git
```

## Prediction experiment: unfinished

[prediction.py](prediction.py) is preserved as an early learning experiment.
Optional dependencies are separated from the plotting setup:

```bash
python -m pip install -r requirements-prediction.txt
```

Installing these dependencies does not make the experiment production-ready:

- It still requests the original Ergast URL. Its data loader needs migration
  to a maintained source such as [Jolpica](https://github.com/jolpica/jolpica-f1/blob/main/docs/README.md),
  including pagination, request timeouts, and explicit error handling.
- Randomly splitting overlapping windows is not a reliable chronological
  evaluation. Use a time-based holdout before interpreting model performance.
- Driver and season are hardcoded. The chosen driver, Liam Lawson, does not
  have the required 15-race history in the selected 2023 season.
- Model output is unconstrained regression, not a calibrated finishing-position
  probability or a validated forecast.

TensorFlow installation also depends on Python version and platform. This
cleanup does not claim a successful end-to-end training run.

## Validation and limitations

The cleanup was checked with Python syntax compilation, cache/ignore-rule
checks, and a headless temperature-plot smoke test with synthetic session data.
The temperature example now creates one reasonably sized figure rather than
an additional enormous blank figure.

Full FastF1 downloads, all six charts against live race data, and TensorFlow
training were not verified in the cleanup environment. This repository remains
a collection of experiments rather than a packaged application.
