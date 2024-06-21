#!/usr/bin/python3
from models.base_model import BaseModel

first_model = BaseModel()
first_model.name = "Football Scout One"
first_model.my_number = 750
print(first_model)
first_model.save()
print(first_model)
first_model_json = first_model.to_dict()
print(first_model_json)
print("JSON of first_model:")
for key in first_model_json.keys():
    print("\t{}: ({}) - {}".format(key, type(first_model_json[key]), first_model_json[key]))
