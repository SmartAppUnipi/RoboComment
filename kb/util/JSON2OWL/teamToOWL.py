#Author: Davide Varagnolo
#Desc: file that allow to generate Club and Team(1718SA) individuals for RoboComment Ontology

import json

JSONFILE = "teams.json"

def writeTeamIndividual (jsonTeam):
    return jsonTeam["name"].replace(" ","")

def writeTeamWyid (jsonTeam):
    return jsonTeam["wyId"]

def writeTeamOfficialName (jsonTeam):
    return jsonTeam["officialName"]

def writeTeamCity (jsonTeam):
    return jsonTeam["city"]

def writeTeamCountry (jsonTeam):
    return jsonTeam["area"]["name"]

def writeTeamType (jsonTeam):
    return jsonTeam["type"]

#Club Individuals
def writeClubToOWL (jsonTeam):
    print("<!-- http://www.semanticweb.org/dvara/ontologies/RoboComment#" + str(writeTeamWyid(jsonTeam)) + " -->")
    print("<owl:NamedIndividual rdf:about=\"http://www.semanticweb.org/dvara/ontologies/RoboComment#" + str(writeTeamWyid(jsonTeam)) + "\">")

    print("\t<rdf:type rdf:resource=\"http://www.semanticweb.org/dvara/ontologies/RoboComment#Club\"/>")
    print("\t<wyid>" + str(writeTeamWyid(jsonTeam)) + "</wyid>")
    print("\t<hasName>" + writeTeamOfficialName(jsonTeam) + "</hasName>")
    print("\t<city>" + writeTeamCity(jsonTeam) + "</city>")
    print("\t<country>" + writeTeamCountry(jsonTeam) + "</country>")
    print("\t<teamType>" + writeTeamType(jsonTeam) + "</teamType>")


    print("</owl:NamedIndividual>\n")
    writeTeamToOWL(jsonTeam)

#Team Individuals
def writeTeamToOWL (jsonTeam):
    print("<!-- http://www.semanticweb.org/dvara/ontologies/RoboComment#" + str(writeTeamWyid(jsonTeam)) + "_1718SA -->")
    print("<owl:NamedIndividual rdf:about=\"http://www.semanticweb.org/dvara/ontologies/RoboComment#" + str(writeTeamWyid(jsonTeam)) + "_1718SA\">")

    print("\t<rdf:type rdf:resource=\"http://www.semanticweb.org/dvara/ontologies/RoboComment#Team\"/>")
    print('\t<inSeason rdf:resource="http://www.semanticweb.org/dvara/ontologies/RoboComment#1718SA"/>')
    print("\t<teamOf rdf:resource=\"http://www.semanticweb.org/dvara/ontologies/RoboComment#" + str(writeTeamWyid(jsonTeam)) + "\"/>")

    print("</owl:NamedIndividual>\n")

# Load Json
with open('../data/' + JSONFILE) as json_file:
    data = json.load(json_file)

for team in data:
    # Only Italian Teams
    if(team["area"]["name"] == "Italy" and team["type"] == "club"):
        writeClubToOWL(team)



