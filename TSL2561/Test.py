import TSL2561_Driver

             				# Power On
Lux, Full, Infrared, Visible = TSL2561_Driver.readLux(0)


# Return values


text_file = open("Light_sensor_output.txt","w+")

print "Lux: %d" %Lux
print "Full Spectrum Value: %d out of 65535" %Full
print "Infrared Spectrum Value: %d out of 65535" %Infrared
print "Visible Spectrum Value: %d out of 65535" %Visible

text_file.write("Lux: %d \n" %Lux)
text_file.write("Full Spectrum Value: %d out of 65535 \n" %Full)
text_file.write("Infrared Spectrum Value: %d out of 65535\n" %Infrared)
text_file.write("Visible Spectrum Value: %d out of 65535\n" %Visible)



