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

    def getSettings(self, object):
        """
        returns an objects settings as a list of tuples (setting name, list of values)
        object == dirac, tsp, datatable, etc
        """
        settings_list = []
        settings = self.dom.getElementsByTagName(object)[0].getElementsByTagName("settings")[0].getElementsByTagName("setting")
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

    def getSetting(self, object, setting_name):
        """
        Returns a list of settings values for a given setting name

        """
        for x in self.getSettings(object):
            if x[0] == setting_name:
                return x[1]
        return None

    def setSetting(self, object, setting_name, value):
        settings = self.dom.getElementsByTagName(object)[0].getElementsByTagName("settings")[0].getElementsByTagName("setting")
        for setting in settings:
            name = setting.getElementsByTagName("name")[0].childNodes[0].data.strip()
            counter = 0
            if name == setting_name:
                for val in setting.getElementsByTagName("value"):
                    val.childNodes[0].data = str(value[counter])
                    counter += 1


if __name__ == "__main__":
    sp = SettingsParser('../data/config.xml')
    print sp.getSettings("ktsp")
    print sp.getSetting("ktsp","Row Key(genes/probes)")[0]
    #sp.setSetting("datatable","Gene Collision Rule", ["AVE"])
    #sp.writeSettings("test.xml")
