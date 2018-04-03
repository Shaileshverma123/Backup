import numpy
import scipy

#grocery_list = ['Juice', ' Tomato']
grocery_list = {
    "state": {
        "desired": {
            "Lamp":"1",
            "Time": [1,2,3]
        }
    }
}
print(grocery_list["state"]["desired"]["Time"][0])
