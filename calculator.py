"""Core SDESM electrical calculations.

This module contains pure calculation helpers only.
"""

from math import sqrt


# Calculate resistance from the base resistance and the current temperature.
# R0 is the initial resistance, and temperature is the measured temperature in Celsius.
def calculate_resistance(R0, temperature):
	reference_temperature = 20
	alpha = 0.00393
	delta_t = temperature - reference_temperature
	return R0 * (1 + alpha * delta_t)


# Calculate electrical power from current and resistance.
# current is the circuit current in amperes, and resistance is the value from calculate_resistance().
def calculate_power(current, resistance):
	return (current ** 2) * resistance


# Calculate the safe current limit using the maximum safe power and the resistance.
# resistance is the calculated resistance used to estimate the safe operating current.
def calculate_safe_current(resistance):
	max_safe_power = 1000
	return sqrt(max_safe_power / resistance)


# Decide the system status from the current power level.
# power is the calculated electrical power in watts.
def determine_status(power):
	max_safe_power = 1000
	if power < 0.7 * max_safe_power:
		return "SAFE"
	if power <= 0.9 * max_safe_power:
		return "WARNING"
	return "DANGEROUS"


if __name__ == "__main__":
	example_R0 = 12.5
	example_temperature = 45
	example_current = 8.0

	resistance = calculate_resistance(example_R0, example_temperature)
	power = calculate_power(example_current, resistance)
	safe_current = calculate_safe_current(resistance)
	status = determine_status(power)

	print("SDESM Calculator Test")
	print(f"Initial Resistance (R0): {example_R0}")
	print(f"Temperature: {example_temperature} C")
	print(f"Calculated Resistance: {resistance:.4f} ohms")
	print(f"Current: {example_current} A")
	print(f"Calculated Power: {power:.4f} W")
	print(f"Safe Current: {safe_current:.4f} A")
	print(f"Status: {status}")
