#!/usr/bin/python3
from models.base_model import BaseModel

second_model = BaseModel()
second_model.name = "Football_Scout_Two"
second_model.my_number = 300
print(second_model.id)
print(second_model)
second_model.save()
print(type(second_model.created_at))
print("--")
second_model_json = second_model.to_dict()
print(second_model_json)
print("JSON of my_model:")
for key in second_model_json.keys():
    print("\t{}: ({}) - {}".format(key, type(second_model_json[key]), second_model_json[key]))

print("--")
second_new_model = BaseModel(**second_model_json)
print(second_new_model.id)
print(second_new_model)
print(type(second_new_model.created_at))

print("--")
print(second_model is second_new_model)
