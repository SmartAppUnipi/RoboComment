type Callback = (success: any, results: any) => void
type DB = {
    execute(query: string, callback: Callback): void
}

export class Ontologies {
    public static readonly data: DB

    private static extract_id(uri_id: string): number {
        const match = uri_id.match(/#\d+/g)

        if (match === null) {
            throw Error('NOT_MATCHING_ID')
        }

        return Number(match[0].slice(1))
    }

    public static process(results: any[]): any {
        results.forEach(obj =>
            Object.keys(obj)
                .filter(key => obj[key] !== null && obj[key] !== undefined)
                .forEach(key => {
                    switch (obj[key].token) {
                        case 'literal':
                            obj[key] = obj[key].value
                            break
                        case 'uri':
                            try {
                                obj[key] = this.extract_id(obj[key].value)
                            } catch (err) {
                                console.error(err)
                                delete obj[key]
                            }

                            break
                    }
                })
        )
        return results
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
    SELECT (?Club AS ?id) ?country ?city ?name
    WHERE {
        ?Club :wyid "${id}".
        ?Club :country ?country.
        ?Club :city ?city.
        ?Club :hasName ?name.
        ####Club :hasRecord records
    }
    `

    public static readonly get_persona = (id: number) => `
    ${Query.header}
    SELECT (?wyid as ?id) ?name ?club ?height ?date_of_birth
    WHERE {
        ?wyid :wyid "${id}".
        ?wyid :hasName ?name.

        ?CareerStation :isPersona :${id} .
        ?CareerStation :isMember ?isMember.

        ?isMember :teamOf ?teamOf.
        ?teamOf :hasName ?club.

        OPTIONAL {
            ?wyid :height ?height
        } .

        OPTIONAL {
            ?wyid :wasBornOn ?date_of_birth
        }
    }
    `

    public static readonly get_match = (id: number) => `
    ${Query.header}
    SELECT ?team1 ?team2 ?home ?away ?home_score ?away_score ?date
	WHERE{
		:${id} :homeTeam ?team1.
		?team1 :teamOf ?team1a.
		?team1a :hasName ?home.

		:${id} :awayTeam ?team2.
		?team2 :teamOf ?team2a.
		?team2a :hasName ?away.

		:${id} :homeTeamScore ?home_score.
		:${id} :awayTeamScore ?away_score.
		:${id} :date ?date.
    }
    `

    public static readonly get_cup = (id: number) => `
    ${Query.header}
    SELECT (?League AS ?id) ?country ?city ?type ?name
    WHERE{
        ?League :wyid "${id}".
        ?League :country ?country.
        ?League :city ?city.
        ?League :teamType ?type.
        ?League :hasName ?name.
    }`

    public static readonly get_players = (match_id: number) => `
    ${Query.header}
    SELECT  (?wyid AS ?id) ?name ?club ?role
    WHERE
    { :${match_id}  :hasPlayedAsFirstTeam   ?team1 .
        ?team1      :isPersona              ?Persons .
        ?Persons    :wyid                   ?wyid .
        ?Persons    :hasName                ?name .
        ?team1      :isMember               ?Member .
        ?Member     :teamOf                 ?club .
        ?team1      :role                   ?role
    }
    ORDER BY ?teamName ?role
    `
}

//     public static readonly get_match = (id1: number, id2:number, id3:number) => `
//     ${Query.header}
//     SELECT  ?Match
// 	WHERE
//   { ?Match  :homeTeam  ?x .
//     ?x      :teamOf    ?x1 .
//     ?x1     :hasName   "${id1}" .
//     ?Match  :awayTeam  ?y .
//     ?y      :teamOf    ?y1 .
//     ?y1     :hasName   "${id2}" .
//     ?Match  :date      "${id3}"
//   }
    // `
// }
