#Author: Davide Varagnolo
#Desc: file that allow to generate Persona and PlayerCareerStation(1718SA) individuals for RoboComment Ontology

import json

JSONFILE = "players.json"
ITALIANTEAM =[3204, 3157, 3159, 3158, 3315, 3166, 3164, 3165, 3162, 3163, 3161, 3219, 3173, 3172, 3176, 3185, 3187, 3197, 3194, 3193]

def writePersonaIndividual (jsonPersona):
    return jsonPersona["shortName"].replace(" ","")

def writePersonaWyid (jsonPersona):
    return jsonPersona["wyId"]

def writeCurrentTeamWyid (jsonPersona):
    return jsonPersona["currentTeamId"]

def writePersonaName (jsonPersona):
    return jsonPersona["shortName"]

def writePersonaCountry (jsonPersona):
    return jsonPersona["passportArea"]["name"]

def writePersonaBday (jsonPersona):
    return jsonPersona["birthDate"]

def writePersonaHeight (jsonPersona):
    return jsonPersona["height"]

def writePersonaRole (jsonPersona):
    return jsonPersona["role"]["name"]

# Persona Individuals
def writePersonaToOWL (jsonPersona):
    print("<!-- http://www.semanticweb.org/dvara/ontologies/RoboComment#" + str(writePersonaWyid(jsonPersona)) + " -->")
    print("<owl:NamedIndividual rdf:about='http://www.semanticweb.org/dvara/ontologies/RoboComment#" + str(writePersonaWyid(jsonPersona)) + "'>")
    print("<rdf:type rdf:resource='http://www.semanticweb.org/dvara/ontologies/RoboComment#Persona'/>")

    print("\t<wyid>" + str(writePersonaWyid(jsonPersona)) + "</wyid>")
    print("\t<hasName>" + writePersonaName(jsonPersona) + "</hasName>")
    print("\t<wasBornIn>" + writePersonaCountry(jsonPersona) + "</wasBornIn>")
    print("\t<wasBornOn>" + writePersonaBday(jsonPersona) + "</wasBornOn>")
    print("\t<height>" + str(writePersonaHeight(jsonPersona)) + "</height>")


    print("</owl:NamedIndividual>\n")
    writeCareerPlayerToOWL(jsonPersona)

# PlayerCareerStation Individuals
def writeCareerPlayerToOWL(jsonPlayer):
    print("<!-- http://www.semanticweb.org/dvara/ontologies/RoboComment#" + str(writePersonaWyid(jsonPlayer)) + "_1718SA -->")
    print("<owl:NamedIndividual rdf:about='http://www.semanticweb.org/dvara/ontologies/RoboComment#" + str(writePersonaWyid(jsonPlayer)) + "_1718SA'>")
    print("<rdf:type rdf:resource='http://www.semanticweb.org/dvara/ontologies/RoboComment#PlayerCareerStation'/>")

    print('\t<inSeason rdf:resource="http://www.semanticweb.org/dvara/ontologies/RoboComment#1718SA"/>')
    print('\t<isPersona rdf:resource="http://www.semanticweb.org/dvara/ontologies/RoboComment#' + str(writePersonaWyid(jsonPlayer)) + '"/>')
    print('\t<isMember rdf:resource="http://www.semanticweb.org/dvara/ontologies/RoboComment#' + str(writeCurrentTeamWyid(jsonPlayer)) + '_1718SA"/>')
    print("\t<role>" + writePersonaRole(jsonPlayer) + "</role>")


    print("</owl:NamedIndividual>\n")


# Load Json
with open('../data/' + JSONFILE) as json_file:
    data = json.load(json_file)

    for persona in data:
        # Only Italian Teams
        if(persona["currentTeamId"] in ITALIANTEAM):
            #writePlayerPresence(persona)
            writePersonaToOWL(persona)



