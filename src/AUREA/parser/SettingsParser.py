"""
Copyright (C) 2011  N.D. Price Lab

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from xml.dom.minidom import parse
class SettingsParser:
    def __init__(self, xmlFileName):
        self.xmlFileName = xmlFileName
        self.dom = parse(xmlFileName) #must include path

    def writeSettings(self, xmlFileName):
        """
        writes an xml file as a setting file
        """
        f = open(xmlFileName, 'w')
        f.write(self.dom.toprettyxml())
        f.close()

    def getSettings(self, settings_object):
        """
        returns an objects settings as a list of tuples (setting name, list of values)
        object == dirac, tsp, datatable, etc
        """
        settings_list = []
        settings = self.dom.getElementsByTagName(settings_object)[0].getElementsByTagName("settings")[0].getElementsByTagName("setting")
        for setting in settings:
            name = setting.getElementsByTagName("name")[0].childNodes[0].data.strip()
            values = []
            for val in setting.getElementsByTagName("value"):
                if val.getAttribute("type") == "integer":
                    values.append(int(val.childNodes[0].data.strip()))
                if val.getAttribute("type") == "float":
                    values.append(float(val.childNodes[0].data.strip()))
                if val.getAttribute("type") == "boolean":
                    v = val.childNodes[0].data.strip()
                    if v not in [ '0','false','False','f','F']:
                        values.append(True)
                    else:
                        values.append(False)

                if val.getAttribute("type") == "string":
                    values.append(val.childNodes[0].data.strip())
            settings_list.append((name, values))
        return settings_list

    def getSetting(self, settings_object, setting_name):
        """
        Returns a list of settings values for a given setting name

        """
        for x in self.getSettings(settings_object):
            if x[0] == setting_name:
                if setting_name == 'Row Key(genes/probes)':
                    return self._genesProbesCleaner(x[1])
                return x[1]
        return None

    def setSetting(self, settings_object, setting_name, value):
        settings = self.dom.getElementsByTagName(settings_object)[0].getElementsByTagName("settings")[0].getElementsByTagName("setting")
        for setting in settings:
            name = setting.getElementsByTagName("name")[0].childNodes[0].data.strip()
            counter = 0
            if name == setting_name:
                for val in setting.getElementsByTagName("value"):
                    val.childNodes[0].data = str(value[counter])
                    counter += 1

    def addSetting(self, settings_name, name, value, data_type):
        """
        This takes a settings name (i.e. datatable, tsp, etc.)(see workspace/data/config.xml) and adds a new setting.
        settings_obj - (string) prexisting set of settings name
        name - (string) the name of the new setting
        value - (list of strings) the value of the new setting
        data_type - (list of strings) the data type(boolean, integer, float, string) of the new setting
        """
        #get settings node
        settings = self.dom.getElementsByTagName(settings_name)[0].getElementsByTagName("settings")[0]
        #clone first node
        new_node = settings.getElementsByTagName("setting")[0].cloneNode(True)
        #change name
        new_node.getElementsByTagName("name")[0].childNodes[0].data = name
        #copy first value node
        value_node =  new_node.getElementsByTagName("value")[0].cloneNode(True)
        #get rid of old values
        for val in new_node.getElementsByTagName("value"):
            new_node.removeChild(val)
        #now add value nodes we want
        for i,newval in enumerate(value):
            new_value_node = value_node.cloneNode(True)
            new_value_node.childNodes[0].data = newval
            new_value_node.setAttribute("type", data_type[i])
            new_node.appendChild(new_value_node)
        #add setting to settings
        settings.appendChild(new_node)
            
    def _genesProbesCleaner(self, row_key):
        """
        K, this is a dumb hack. Apparently whether a row_key should be 
        'gene' or 'genes' is causing confusion.  I decided to just sanitize
        the output.
        """
        
        if len(row_key) and row_key[0] == 'genes':
            return ['gene']
        if len(row_key) and row_key[0] == 'probes':
            return ['probe']
        return row_key
            

if __name__ == "__main__":
    sp = SettingsParser('/home/earls3/Price/AUREA/workspace/data/config.xml')
    print sp.getSettings("datatable")
    sp.addSetting("datatable", "csvsettings", ["IDENTIFIER", "ID_REF"], ["string", "string"])
    print sp.getSetting("datatable", "csvsettings")
    sp.writeSettings("test.xml")
    #sp.setSetting("datatable","Gene Collision Rule", ["AVE"])
    #sp.writeSettings("test.xml")
