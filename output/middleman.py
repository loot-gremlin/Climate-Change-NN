import keras
from keras.models import load_model
import sys

days = int(sys.argv[1])
state = str(sys.argv[2])
city = str(sys.argv[3])

file = state + " " + city
file += ".h5"
model = load_model(file)
predictions = model.predict([[days]])
predictions = list(predictions[0])
temp = int(predictions[0])
precip = int(predictions[1])
if precip < 0:
    precip = 0
humidity = int(predictions[2])
print("Temperature (F):", temp, "Precipitation (in):", precip, "Humidity (%):", humidity)
