#Author: Davide Varagnolo
#Desc: file that allow to generate Match(1718SA) individuals for RoboComment Ontology
import json

JSONFILE = "matches_Italy.json"


def writeMatchWyid (jsonMatch):
    return jsonMatch["wyId"]

def writeMatchDate (jsonMatch):
    return jsonMatch["date"]

def writeMatchScore(jsonMatch, team):
    return jsonMatch["teamsData"][team]["score"]

# Match Individuals
def writeMatchToOWL (jsonMatch, homeTeamId, awayTeamId):

    print("<!-- http://www.semanticweb.org/dvara/ontologies/RoboComment#" + str(writeMatchWyid(jsonMatch)) + " -->")
    print("<owl:NamedIndividual rdf:about='http://www.semanticweb.org/dvara/ontologies/RoboComment#" + str(writeMatchWyid(jsonMatch)) + "'>")
    print("<rdf:type rdf:resource='http://www.semanticweb.org/dvara/ontologies/RoboComment#Match'/>")

    print('\t<homeTeam rdf:resource="http://www.semanticweb.org/dvara/ontologies/RoboComment#' + homeTeamId + '_1718SA"/>')
    print('\t<awayTeam rdf:resource="http://www.semanticweb.org/dvara/ontologies/RoboComment#' + awayTeamId + '_1718SA"/>')
    print('\t<inSeason rdf:resource="http://www.semanticweb.org/dvara/ontologies/RoboComment#1718SA"/>')
    print("\t<homeTeamScore>" + str(writeMatchScore(jsonMatch, homeTeamId)) + "</homeTeamScore>")
    print("\t<awayTeamScore>" + str(writeMatchScore(jsonMatch, awayTeamId)) + "</awayTeamScore>")
    print("\t<date>" + str(writeMatchDate(jsonMatch)) + "</date>")
    # PlayerCareerStation has played that Match
    for player in jsonMatch["teamsData"][homeTeamId]["formation"]["lineup"]:
        print('\t<hasPlayedAsFirstTeam rdf:resource="http://www.semanticweb.org/dvara/ontologies/RoboComment#' + str(player["playerId"]) + '_1718SA"/>')
    for player in jsonMatch["teamsData"][awayTeamId]["formation"]["lineup"]:
        print('\t<hasPlayedAsFirstTeam rdf:resource="http://www.semanticweb.org/dvara/ontologies/RoboComment#' + str(player["playerId"]) + '_1718SA"/>')


    print("</owl:NamedIndividual>\n")

# Load Json
with open('../data/' + JSONFILE) as json_file:
    data = json.load(json_file)

#for team in data[45]["teamsData"]:
#writeMatchToOWL(data[0])

for Match in data:
    # Matches of Juve and Inter
    for team in Match["teamsData"]:
        if (Match["teamsData"][team]['side'] == "home"):
            homeTeamId = team
        else:
            awayTeamId = team
    if (awayTeamId == ("3161" or "3159") or homeTeamId == ("3161" or "3159")):
        writeMatchToOWL(Match, homeTeamId, awayTeamId)



