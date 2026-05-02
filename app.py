from flask import Flask, render_template, request, jsonify
import math

from calculator import (
    calculate_resistance,
    calculate_power,
    calculate_safe_current,
    determine_status,
)
from alerts import generate_alerts
from data_storage import save_record, load_history


app = Flask(__name__)


# Main page route: serve the SDESM frontend.
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# Analysis route: accept JSON input, run calculations, save a history record, and return results.
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()

        # Read inputs and convert numeric values to float where appropriate
        temperature = float(data.get("temperature"))
        wind_speed = float(data.get("wind_speed"))
        humidity = float(data.get("humidity"))
        weather = data.get("weather")
        R0 = float(data.get("resistance"))
        current = float(data.get("current"))
        voltage = float(data.get("voltage"))

        # Perform calculations using the calculator module
        resistance = calculate_resistance(R0, temperature)
        power = calculate_power(current, resistance)
        safe_current = calculate_safe_current(resistance)
        status = determine_status(power)

        # Generate alerts based on status and environment
        alerts = generate_alerts(status, humidity, temperature, wind_speed)

        # Save the record to CSV (alerts are joined into a single string)
        alerts_str = " | ".join(alerts)
        save_record(temperature, wind_speed, humidity, weather, resistance, power, safe_current, status, alerts_str)

        # Return the results as JSON
        return jsonify(
            resistance=resistance,
            power=power,
            safe_current=safe_current,
            status=status,
            alerts=alerts,
        )

    except Exception as e:
        return jsonify(error=str(e)), 500


if __name__ == "__main__":
    app.run(debug=True)
