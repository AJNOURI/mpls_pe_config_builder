#!/usr/bin/env python

import yaml
import jinja2

stream = open("STATIC-MPLS.yaml",'r')
vars = yaml.load(stream)

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('pe.txt')
print template.render(vars)
