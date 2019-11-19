
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
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX info: <http://somewhere/peopleInfo#>
    PREFIX vcard: <http://www.w3.org/2001/vcard-rdf/3.0#>
    PREFIX : <http://www.semanticweb.org/dvara/ontologies/RoboComment#>`

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
    SELECT ?name ?wasBornIn ?club ?height ?wasBornOn
    WHERE {
        ?wyid :wyid "${id}".
        ?wyid :hasName ?name.

        OPTIONAL {
            ?wyid :height ?heightS
        } .

        OPTIONAL {
            ?wyid :wasBornIn ?wasBornIn
        } .

        OPTIONAL {
            ?wyid :wasBornOn ?wasBornOn
        }
    }
    `

    // public static readonly get_persona = (id: number) => `
    // ${Query.header}
    // SELECT ?name ?wasBornIn ?club ?wasBornOn
    // WHERE {
    //     ?wyid :wyid "${id}".
    //     ?wyid :hasName ?name.
    //     ?wyid :wasBornIn ?wasBornIn.
    //     ?wyid :wasBornOn ?wasBornOn.

    //     ?CoachCareerStation :isPersona :${id} .
    //     ?CoachCareerStation :isMember ?isMember.

    //     ?isMember :teamOf ?teamOf.
    // }
    // `

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
