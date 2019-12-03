#Author: Davide Varagnolo
#Desc: file that allow to generate Persona and CoachCareerStation(1718SA) individuals for RoboComment Ontology

import json

JSONFILE = "coaches.json"
ITALIANTEAM =[3204, 3157, 3159, 3158, 3315, 3166, 3164, 3165, 3162, 3163, 3161, 3219, 3173, 3172, 3176, 3185, 3187, 3197, 3194, 3193]

def writeCoachIndividual (jsonCoach):
    return jsonCoach["shortName"].replace(" ","")

def writeCoachWyid (jsonCoach):
    return jsonCoach["wyId"]

def writeCurrentTeamWyid (jsonCoach):
    return jsonCoach["currentTeamId"]

def writeCoachName (jsonCoach):
    return jsonCoach["shortName"]

def writeCoachCountry (jsonCoach):
    return jsonCoach["passportArea"]["name"]

def writeCoachBday (jsonCoach):
    return jsonCoach["birthDate"]

# Persona Individuals
def writeCoachToOWL (jsonCoach):
    print("<!-- http://www.semanticweb.org/dvara/ontologies/RoboComment#" + str(writeCoachWyid(jsonCoach)) + " -->")
    print("<owl:NamedIndividual rdf:about='http://www.semanticweb.org/dvara/ontologies/RoboComment#" + str(writeCoachWyid(jsonCoach)) + "'>")
    print("<rdf:type rdf:resource='http://www.semanticweb.org/dvara/ontologies/RoboComment#Persona'/>")

    print("\t<wyid>" + str(writeCoachWyid(jsonCoach)) + "</wyid>")
    print("\t<hasName>" + writeCoachName(jsonCoach) + "</hasName>")
    print("\t<wasBornIn>" + writeCoachCountry(jsonCoach) + "</wasBornIn>")
    print("\t<wasBornOn>" + writeCoachBday(jsonCoach) + "</wasBornOn>")

    print("</owl:NamedIndividual>\n")
    writeCareerPlayerToOWL(jsonCoach)

# CoachCareerStation Individuals
def writeCareerPlayerToOWL(jsonCoach):
    print("<!-- http://www.semanticweb.org/dvara/ontologies/RoboComment#" + str(writeCoachWyid(jsonCoach)) + "_1718SA -->")
    print("<owl:NamedIndividual rdf:about='http://www.semanticweb.org/dvara/ontologies/RoboComment#" + str(writeCoachWyid(jsonCoach)) + "_1718SA'>")
    print("<rdf:type rdf:resource='http://www.semanticweb.org/dvara/ontologies/RoboComment#CoachCareerStation'/>")

    print('\t<isPersona rdf:resource="http://www.semanticweb.org/dvara/ontologies/RoboComment#' + str(writeCoachWyid(jsonCoach)) + '"/>')
    print('\t<inSeason rdf:resource="http://www.semanticweb.org/dvara/ontologies/RoboComment#1718SA"/>')
    print('\t<isMember rdf:resource="http://www.semanticweb.org/dvara/ontologies/RoboComment#' + str(writeCurrentTeamWyid(jsonCoach)) + '"/>')

    print("</owl:NamedIndividual>\n")


# Load Json
with open('../data/' + JSONFILE) as json_file:
    data = json.load(json_file)

    for Coach in data:
        # Only Italian Teams
        if(Coach["currentTeamId"] in ITALIANTEAM):
            writeCoachToOWL(Coach)
            #print(writeCoachName(Coach))


