from flask import Flask, render_template
import fastf1
import matplotlib.pyplot as plt
from fastf1 import plotting
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    # Download the data for a specific session (e.g., the 2023 Bahrain Grand Prix)
    session = fastf1.get_session(2023, 'Bahrain', 'FP1')
    
    # Load the data (this is the practice session)
    session.load()

    # Access telemetry data for a specific driver (e.g., Max Verstappen)
    driver_data = session.laps.pick_driver('VER')

    # Create the plot for telemetry data
    fig, ax = plt.subplots(figsize=(10, 6))
    driver_data.plot_track(ax=ax)

    # Save the plot to a byte buffer and encode it as a base64 string
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    # Render the HTML page and pass the plot URL to it
    return render_template('index.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)

