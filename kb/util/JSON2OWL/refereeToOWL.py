#Author: Davide Varagnolo
#Desc: file that allow to generate Persona and RefereeCareerStation(1718SA) individuals for RoboComment Ontology

import json

JSONFILE = "referees.json"
ITALIANTEAM =[3204, 3157, 3159, 3158, 3315, 3166, 3164, 3165, 3162, 3163, 3161, 3219, 3173, 3172, 3176, 3185, 3187, 3197, 3194, 3193]

def writeRefereeIndividual (jsonReferee):
    return jsonReferee["shortName"].replace(" ","")

def writeRefereeWyid (jsonReferee):
    return jsonReferee["wyId"]

def writeCurrentTeamWyid (jsonReferee):
    return jsonReferee["currentTeamId"]

def writeRefereeName (jsonReferee):
    return jsonReferee["shortName"]

def writeRefereeCountry (jsonReferee):
    return jsonReferee["passportArea"]["name"]

def writeRefereeBday (jsonReferee):
    return jsonReferee["birthDate"]

# Persona Individuals
def writeRefereeToOWL (jsonReferee):
    print("<!-- http://www.semanticweb.org/dvara/ontologies/RoboComment#" + str(writeRefereeWyid(jsonReferee)) + " -->")
    print("<owl:NamedIndividual rdf:about='http://www.semanticweb.org/dvara/ontologies/RoboComment#" + str(writeRefereeWyid(jsonReferee)) + "'>")
    print("<rdf:type rdf:resource='http://www.semanticweb.org/dvara/ontologies/RoboComment#Persona'/>")

    print("\t<wyid>" + str(writeRefereeWyid(jsonReferee)) + "</wyid>")
    print("\t<hasName>" + writeRefereeName(jsonReferee) + "</hasName>")
    print("\t<wasBornIn>" + str(writeRefereeCountry(jsonReferee)) + "</wasBornIn>")
    print("\t<wasBornOn>" + str(writeRefereeBday(jsonReferee)) + "</wasBornOn>")

    print("</owl:NamedIndividual>\n")
    writeCareerPlayerToOWL(jsonReferee)

# RefereeCareerStation Individuals
def writeCareerPlayerToOWL(jsonReferee):
    print("<!-- http://www.semanticweb.org/dvara/ontologies/RoboComment#" + str(writeRefereeWyid(jsonReferee)) + "_1718SA -->")
    print("<owl:NamedIndividual rdf:about='http://www.semanticweb.org/dvara/ontologies/RoboComment#" + str(writeRefereeWyid(jsonReferee)) + "_1718SA'>")
    print("<rdf:type rdf:resource='http://www.semanticweb.org/dvara/ontologies/RoboComment#RefereeCareerStation'/>")

    print('\t<isPersona rdf:resource="http://www.semanticweb.org/dvara/ontologies/RoboComment#' + str(writeRefereeWyid(jsonReferee)) + '"/>')
    print('\t<inSeason rdf:resource="http://www.semanticweb.org/dvara/ontologies/RoboComment#1718SA"/>')

    print("</owl:NamedIndividual>\n")


# Load Json
with open('../data/' + JSONFILE) as json_file:
    data = json.load(json_file)

    for Referee in data:
        writeRefereeToOWL(Referee)



