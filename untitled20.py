#DOPPLER EFFECT
def doppler_detective(wavelength1, wavelength2):
    if wavelength2 > wavelength1:
        doppler_velocity = ((wavelength2-wavelength1)/(wavelength1))*(2.99 * 10 ** 18) #Angstroms per second.
        radial_velocity = doppler_velocity * (10 ** -10)
        return(radial_velocity)
        print(str(radial_velocity) + "m/s")
        