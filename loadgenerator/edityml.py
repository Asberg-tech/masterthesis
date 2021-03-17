#!/usr/bin/env python3

import yaml
import sys

def yaml_loader(filepath):
    with open(filepath) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


def yaml_editor(data, usernumber):
    print(data)

    # print(yaml.dump(data))
    var = data["spec"]["template"]["spec"]["containers"]
    envlist = var[0]
    env = envlist["env"]
    users = env[1]
    users["value"] = usernumber
    env[1] = users
    envlist["env"] = env
    var[0] = envlist
    data["spec"]["template"]["spec"]["containers"] = var
    print(yaml.dump(data))
    return data


def save_yaml(newdata):
    with open("test.yaml", "w") as file:
        document = yaml.dump(newdata, file)


def edit_yaml(usernumber):
    filepath = 'loadgenerator.yaml'
    data = yaml_loader(filepath)
    newdata = yaml_editor(data, str(usernumber))
    save_yaml(newdata)

# if __name__ == "__main__":
#     print(sys.argv[1:][0])
#     usernumber = sys.argv[1:][0]
#     filepath = 'loadgenerator.yaml'
#     data = yaml_loader(filepath)
#     newdata = yaml_editor(data, str(usernumber))
#     save_yaml(newdata)

    
     








