#!/usr/bin/env python

import yaml
import jinja2

stream = open("./templates/static-mpls-vpn/static-mpls-vpn-pe.yaml",'r')
vars = yaml.load(stream)

env = Environment(loader=FileSystemLoader('../templates/static-mpls-vpn/'))
template = env.get_template('pe.txt')
print template.render(vars)
