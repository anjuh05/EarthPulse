# EarthPulse

EarthPulse is a student-built dashboard for exploring historical temperature and precipitation data from NASA POWER.

## Features
- Select an Indian location from the sidebar.
- Request daily temperature (T2M) and corrected precipitation (PRECTOTCORR).
- View monthly temperature averages and monthly precipitation totals.
- Inspect and download the daily data as CSV.

## Data source
NASA POWER Daily Point API:
https://power.larc.nasa.gov/docs/services/api/temporal/daily/

Parameters used:
- `T2M`: temperature at 2 metres (°C)
- `PRECTOTCORR`: corrected precipitation (mm/day)

The dashboard aggregates daily values into monthly summaries. Monthly precipitation is calculated as the sum of daily values. Data availability and quality can vary by location and date.

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install dependencies:

   `python -m pip install -r requirements.txt`

4. Start the app:

   `python -m streamlit run app.py`

5. Open the local URL shown in the terminal (usually http://localhost:8501).

An internet connection is required to retrieve data from NASA POWER.

## Notes
This is a starter implementation. Test the app, verify the returned data, and make sure the team understands and can explain the analysis before submitting. Add team-authored improvements and screenshots before publishing the repository.
