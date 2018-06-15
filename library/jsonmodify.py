#!/usr/bin/python

import json

# A recursive function that sets the specified value into the given JSON object.
#
# TODO: Modify this function so that if the path element is a number, then treat
#       the outer-most JSON object as a list with the number being the index.
def set_json_value(json, path_list, new_value):

    if len(path_list) > 1:
        outer_most_path_element = path_list.pop(0)

        try:
            sub_json_object = json[outer_most_path_element]
            set_json_value(sub_json_object, path_list, new_value)
        except KeyError as error:
            raise KeyError('No JSON entry with value ' + outer_most_path_element)
    else:
        json[path_list[0]] = new_value
