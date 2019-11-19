
type DB = {
    execute(query: string, callback: (success: any, results: any) => void): void
}
export class Ontologies {
    public static readonly data: DB

    public static process(obj: any): any {
        obj = obj[0]

        Object.keys(obj).forEach(key => {
            switch (obj[key].token) {
                case 'literal':
                    obj[key] = obj[key].value
                    break
                case 'uri':
                    delete obj[key]
                    break
            }
        })

        return obj
    }
}

// tslint:disable-next-line: max-classes-per-file
export class Query {

    private static readonly header: string = `
    PREFIX : <http://www.semanticweb.org/dvara/ontologies/RoboComment#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>`

    public static readonly get_club = (id: number) => `
    ${Query.header}
    SELECT *
    WHERE {
        ?Club :wyid "${id}".
        ?Club :country ?country.
        ?Club :city ?city.
        ?Club :hasName ?hasName.
        ####Club :hasRecord records
    }
    `

    public static readonly get_persona = (id: number) => `
    ${Query.header}
    SELECT ?hasPlayerName ?wasBornIn ?teamName ?height ?wasBornOn
    WHERE {
        ?wyid :wyid "${id}".
        ?wyid :hasName ?hasPlayerName.
        ?wyid :wasBornIn ?wasBornIn.
        ?wyid :height ?height.
        ?wyid :wasBornOn ?wasBornOn.

        ?PlayerCareerStation :isPersona :${id}.
        ?PlayerCareerStation :isMember ?isMember.

        ?isMember :teamOf ?teamOf.
        ?teamOf :hasName ?teamName.
    }
    `

    public static readonly get_match = (id: number) => `
    ${Query.header}
    SELECT ?homeTeamName ?awayTeamName ?homeTeamScore ?awayTeamScore ?date
    WHERE {
        :2575959 :homeTeam ?team1.
        ?team1 :hasName ?homeTeamName.
        :2575959 :awayTeam ?team2.
        ?team2 :hasName ?awayTeamName.
        :2575959 :homeTeamScore ?homeTeamScore.
        :2575959 :awayTeamScore ?awayTeamScore.
        :2575959 :date ?date.
    }
    `

    public static readonly get_cup = (id: number) => `
    ${Query.header}
    SELECT ?##info(season)
    WHERE
        ?Season :hasCup "Coppa Italia"
        ?Season :cupWinner ?Winner
        ?Season :runnerUP ?runnerUP
    `
    // 3157
}
