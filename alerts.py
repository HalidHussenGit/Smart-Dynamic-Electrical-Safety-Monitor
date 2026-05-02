"""Alert generation helpers for SDESM.

This module contains pure logic for converting analysis results into alerts.
"""


# Generate alert messages from the current system status and environmental conditions.
# status is the electrical status, humidity is the relative humidity percentage,
# temperature is the ambient temperature in Celsius, and wind_speed is the cooling air speed.
def generate_alerts(status, humidity, temperature, wind_speed):
	alerts = []

	# A dangerous power level can overheat wiring and equipment, so shutdown guidance is critical.
	if status == "DANGEROUS":
		alerts.append("CRITICAL: System overheating — Shut down immediately recommended")

	# A warning status means the load is close to unsafe limits and should be reduced before damage occurs.
	if status == "WARNING":
		alerts.append("WARNING: Reduce current load by 25% to avoid overheating")

	# High humidity can reduce insulation resistance and increase leakage or short-circuit risk.
	if humidity > 80:
		alerts.append("RISK: High humidity detected — Check insulation integrity")

	# Extreme heat can accelerate conductor heating and push components toward thermal failure.
	if temperature > 60:
		alerts.append("RISK: Extreme temperature — Thermal limit approaching")

	# Low wind speed weakens natural cooling, which can let cables and connectors retain heat.
	if wind_speed < 2:
		alerts.append("NOTICE: Low wind speed — Reduced cooling effect on line")

	if not alerts:
		return ["All conditions normal — System operating safely"]

	return alerts


if __name__ == "__main__":
	scenarios = [
		("SAFE", 45, 30, 5),
		("WARNING", 85, 62, 1.5),
		("DANGEROUS", 70, 40, 3),
	]

	print("SDESM Alert Generator Test")
	for index, scenario in enumerate(scenarios, start=1):
		status, humidity, temperature, wind_speed = scenario
		print(f"Scenario {index}: status={status}, humidity={humidity}, temperature={temperature}, wind_speed={wind_speed}")
		print(generate_alerts(status, humidity, temperature, wind_speed))
