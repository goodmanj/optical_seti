def laser_power_threshold(wave, flux_threshold, distance):
    initial_power = ((flux_threshold) * (1.22 ** 2) * (3.14159) * (6.626E-34) * (2.99E8) * (5812 * (1E-10)) * ((distance * (3.086E16)) ** 2)) / (400 * 36.31 * 600 * .05)
    megawatt_converted = initial_power / (1000000)
    return megawatt_converted
    print(megawatt_converted)

