"""Driver Program for Main Car Finder Application Funcionality"""


class Car:
    def __init__(self, id, model, color, manufacturer, price, car_type, usage, mileage, miles_per_gal, nearest_dealership, transmission_type, fuel_type):
        self.id = id
        self.model = model
        self.color = color
        self.manufacturer = manufacturer
        self.price = price
        self.type = car_type
        self.use = usage
        self.mileage = mileage
        self.miles_per_gal = miles_per_gal
        self.nearest_dealership = nearest_dealership
        self.transmission_type = transmission_type
        self.fuel_type = fuel_type

    def to_dict(self):
        return {
            'id': self.id,
            'model': self.model,
            'color': self.color,
            'manufacturer': self.manufacturer,
            'price': self.price,
            'type': self.type,
            'use': self.use,
            'mileage': self.mileage,
            'miles_per_gal': self.miles_per_gal,
            'nearest_dealership': self.nearest_dealership,
            'transmission_type': self.transmission_type,
            'fuel_type': self.fuel_type,
        }
    

class main_car_List:
    def __init__(self):
        clist = []

    def add_car(car,self):
        self.clist.append(car)

    def get_all_cars(self):
        return [car.to_dict() for car in self.clist]          


