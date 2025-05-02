# 🚀 Mars Weather

This is a Dash-based web application that visualizes Mars exploration data using NASA's public APIs and static planetary datasets.

## 🧩 Features

- 📸 Fetch and display **NAVCAM images** from NASA's Mars rovers.
- 🌡️ Visualize **temperature and pressure data** from the InSight lander.
- 🌍 Compare **global climate maps** of Earth and Mars (static images).
- 📅 Interactive date selection and dynamic updates.

## 🛠️ Requirements

- Python 3.8+
- See `requirements.txt` for package dependencies

## References

- Earth topography map https://visibleearth.nasa.gov/images/57752/blue-marble-land-surface-shallow-water-and-shaded-topography
- Mars topography map https://www.jpl.nasa.gov/images/pia17357-nasas-mars-landing-sites-including-insight/

## 🧑‍💻 How to Run

```bash
# 1. 環境を準備（Python 3.8以上を推奨）
# Clone the repository
git clone https://github.com/iked-y/mars-explorer-dashboard.git
cd mars-explorer-dashboard

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# 2. アプリを起動
# Run the Dash app
python app.py

# 3. ブラウザでアクセス
表示されたURL（通常は http://127.0.0.1:8050/）を開くと、Webアプリが起動します。