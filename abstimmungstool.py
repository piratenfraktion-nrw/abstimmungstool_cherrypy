#/bin/python
# -*- coding: utf-8 -*-

__author__    = 'Gerrit Giehl <ggiehl@piratenfraktion-nrw.de>'
__contact__   = 'it@piratenfraktion-nrw.de'
__date__      = '07 November 2014'

import cherrypy
import os.path
import operator
from models.top import Top
from genshi.template import TemplateLoader
from pyactiveresource.activeresource import ActiveResource
from pyactiveresource import formats
from lib import template

APPDIR = os.path.dirname(os.path.abspath(__file__))
CONFIGFILE = os.path.join(APPDIR, 'server.conf')

class Abstimmungstool(object):

    @cherrypy.expose
    @template.output('index.html') 
    def index(self):

        tops = []

        issues = Issue.find(query_id = 67)
        for i, v in enumerate(issues):
            t = Top()
            #print('issue [',i,']',' =', v)
            for item in issues[i].attributes:
                #print(item, " = ", issues[i].attributes[item])
                if item == 'custom_fields':
                    for j, cf in enumerate(issues[i].attributes[item]):
                        #print(cf, " = ", cf.attributes['name'])
                        if cf.attributes['name'] == 'Abstimmungsempfehlung':
                            t.abstimmungsempfehlung = cf.attributes['value']
                            if t.abstimmungsempfehlung == 'Dafür':
                                t.btn = 'btn-success'
                            elif t.abstimmungsempfehlung == 'Dagegen':
                                t.btn = 'btn-danger'
                            elif t.abstimmungsempfehlung == 'Zustimmung zur Überweisung':
                                t.btn = 'btn-warning'
                            elif t.abstimmungsempfehlung == 'Enthaltung':
                                t.btn = 'btn-primary'
                            else:
                                t.btn = 'btn-default'

                        elif cf.attributes['name'] == 'Top':
                            t.nummer = int(cf.attributes['value'])

                elif item == 'id':
                    t.ticketid = issues[i].attributes[item]
                elif item == 'subject':
                    t.beschreibung = issues[i].attributes[item]
            tops.append(t)
            del t

        tops.sort(key=operator.attrgetter("nummer"), reverse=False)
        
        return template.render(tops=tops)


class Issue(ActiveResource):
    _site = 'https://redmine.piratenfraktion-nrw.de/projects/plenum'
    _format = formats.XMLFormat  

def main():
    cherrypy.quickstart(Abstimmungstool(), config = CONFIGFILE)
    #cherrypy.root = Abstimmungstool()
    #cherrypy.config.update(CONFIGFILE)
    #cherrypy.server.start()

if __name__ == "__main__":
    main()
