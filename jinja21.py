#!/usr/bin/env python

__author__ = 'AJ NOURI'
__date__ = '19/08/14'
__license__ = ''
__version__ = ''
__email__ = 'ajn.bin@gmail.com'


'''

### NOW
### 1.working PE-MPLSVPN-STATIC

### TODO
### 1.add multiple customer vrfs per PE:
###     definition
###     pe-ce interface
###     route to CE network
### 2.Make class/object-based :
###     variable initialisation method
###     template parser method
###     config maker method
###     yield method standard / file output
### 3.PE-CE dynamic routing :
###     choice between OSPF / EIGRP / BGP
###     template parser method
###     config maker method
###     yield method standard / file output
### 4.Get the list of interface numbers and check yaml interfacs
### 5.check IP addresses format and calculate subnets and hosts:
        netaddr 0.7.12:     https://pythonhosted.org/netaddr/
'''


from jinja2 import Environment, FileSystemLoader, Template
import yaml
from optparse import *

### Option parsing
usage = "usage: %prog [options] arg1 arg2"
parser = OptionParser(usage=usage)

#------------ Help group inf.
group = OptionGroup(parser, "YAML Source file information:",
                    "By default the program gets source inf. from: STATIC-MPLS.yaml")
group.add_option("-s", "--source", dest="sourcefile", default="STATIC-MPLS.yaml", help="Specify the source file.")
parser.add_option_group(group)

#------------ Help group inf.
group = OptionGroup(parser, "PE-CE routing options:",
                    "The default PE-CE routing is static")
group.add_option("-r", "--routing", dest="pecerouting", default="static", help="Specify PE-CE routing type.")
parser.add_option_group(group)

#------------ Help group inf.
group = OptionGroup(parser, "Template file information:",
                    "By default the program reads the file: pe.txt")
group.add_option("-t", "--template", dest="templatefile", default="pe.txt", help="Specify the template file.")
parser.add_option_group(group)

#------------ Parsing arguments
(options, args) = parser.parse_args()

#--------------JINJA2
#TEMPLATE_DIR = '~/Dropbox/coding/python/jinja2'

#TEMPLATE_DIR = '.'
#env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
#template = env.get_template('hello.html')

#todo_list = ["Watch TV", "Contemplate Work", "Go to Bed"]
#todi_list = ["aaa", "bbb", "ccc"]

#print template.render(todos=todo_list, todis=todi_list)


#------------- Assign files from parsed argument
TEMPLATE_DIR = '.'
TEMPLATE_FILE = options.templatefile
yamltopo = options.sourcefile
pecerouting = options.pecerouting
print 'PE-CE Routing is %s' % pecerouting


class YamlChecker(object):
    def __init__(self, yamltopofile, templatefile):
        self.yamltopofile = yamltopofile
        self.template = templatefile
        self.stream = file(yamltopofile, 'r')
        self.datadict = yaml.load(self.stream)

    def VarValidator(self):
        for pe_nbr in xrange(0, len(Yamlo.datadict)):
            # Parameters from source YAML file
            hostname = self.datadict[pe_nbr]['hostname']
            custVrfName = self.datadict[pe_nbr]['vrf']['custVrfName']
            custVrfId = self.datadict[pe_nbr]['vrf']['custVrfId']
            custVrfAs = self.datadict[pe_nbr]['vrf']['custVrfAs']
            peCeInt = self.datadict[pe_nbr]['peceinterface']['peCeInt']
            peCeSubnet = self.datadict[pe_nbr]['peceinterface']['peCeSubnet']
            peCeMask = self.datadict[pe_nbr]['peceinterface']['peCeMask']
            peCehost = self.datadict[pe_nbr]['peceinterface']['peCehost']
            loInt = self.datadict[pe_nbr]['loopback']['loInt']
            loMask = self.datadict[pe_nbr]['loopback']['loMask']
            loSubnet = self.datadict[pe_nbr]['loopback']['loSubnet']
            lohost = self.datadict[pe_nbr]['loopback']['lohost']
            ospfId = self.datadict[pe_nbr]['coreinterface']['ospfId']
            coreOspfArea = self.datadict[pe_nbr]['coreinterface']['coreOspfArea']
            coreInt = self.datadict[pe_nbr]['coreinterface']['coreInt']
            coreSubnet = self.datadict[pe_nbr]['coreinterface']['coreSubnet']
            corehost = self.datadict[pe_nbr]['coreinterface']['corehost']
            coreMask = self.datadict[pe_nbr]['coreinterface']['coreMask']
            coreBgpAs = self.datadict[pe_nbr]['corebgp']['coreBgpAs']
            rrIP = self.datadict[pe_nbr]['corebgp']['rrIP']
            ceIp = self.datadict[pe_nbr]['staticroute']['ceIp']
            routerid = self.datadict[pe_nbr]['routerid']


            if not isinstance(hostname, int):
                raise TypeError("hostname represent the number of PE router, so should be an integer")
            elif not isinstance(custVrfName, str):
                raise TypeError("custVrfName must be a string")
            elif not isinstance(custVrfId, int):
                raise TypeError("custVrfId must be an integer")
            elif not isinstance(peCeInt, str):
                raise TypeError("peCeInt must be a string")
            elif not isinstance(peCeSubnet, str):
                raise TypeError("peCeSubnet must be a string")
            elif not isinstance(peCeMask, str):
                raise TypeError("peCeMask must be a string")
            elif not isinstance(peCehost, int):
                raise TypeError("peCehost must be an integer")


            else:
                    ### Print parsed template to standard output
                    print self.template.render(datalist=self.datadict[pe_nbr])
                    #print '#####################'

                    ### Print parsed template to a configuration file
                    with open("PE"+str(self.datadict[pe_nbr]['hostname'])+".cfg", "wb") as conf_file:
                        conf_file.write(self.template.render(datalist=self.datadict[pe_nbr]))


mpls_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
pe_template = mpls_env.get_template(TEMPLATE_FILE)


Yamlo =  YamlChecker(yamltopo, pe_template)
# print dictionary from yaml file
print Yamlo.datadict
Yamlo.VarValidator()



#-------------- Assign variables
'''
for pe_nbr in xrange(0, len(Yamlo.datadict)):
    # Parameters from source YAML file
    hostname = datadict[pe_nbr]['hostname']
    custVrfName = datadict[pe_nbr]['vrf']['custVrfName']
    custVrfId = datadict[pe_nbr]['vrf']['custVrfId']
    custVrfAs = datadict[pe_nbr]['vrf']['custVrfAs']
    peCeInt = datadict[pe_nbr]['peceinterface']['peCeInt']
    peCeSubnet = datadict[pe_nbr]['peceinterface']['peCeSubnet']
    peCeMask = datadict[pe_nbr]['peceinterface']['peCeMask']
    peCehost = datadict[pe_nbr]['peceinterface']['peCehost']
    loInt = datadict[pe_nbr]['loopback']['loInt']
    loMask = datadict[pe_nbr]['loopback']['loMask']
    loSubnet = datadict[pe_nbr]['loopback']['loSubnet']
    lohost = datadict[pe_nbr]['loopback']['lohost']
    ospfId = datadict[pe_nbr]['coreinterface']['ospfId']
    coreOspfArea = datadict[pe_nbr]['coreinterface']['coreOspfArea']
    coreInt = datadict[pe_nbr]['coreinterface']['coreInt']
    coreSubnet = datadict[pe_nbr]['coreinterface']['coreSubnet']
    corehost = datadict[pe_nbr]['coreinterface']['corehost']
    coreMask = datadict[pe_nbr]['coreinterface']['coreMask']
    coreBgpAs = datadict[pe_nbr]['corebgp']['coreBgpAs']
    rrIP = datadict[pe_nbr]['corebgp']['rrIP']
    ceIp = datadict[pe_nbr]['staticroute']['ceIp']
    routerid = datadict[pe_nbr]['routerid']

    ### Print parsed template to standard output
    print pe_template.render(datalist=Yamlo.datadict[pe_nbr])
    print '#####################'

    ### Print parsed template to a configuration file
    with open("PE"+str(Yamlo.datadict[pe_nbr]['hostname'])+".cfg", "wb") as conf_file:
        conf_file.write(pe_template.render(datalist=Yamlo.datadict[pe_nbr]))

'''

