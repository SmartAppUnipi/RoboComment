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

    public static process(obj: any): any {
        console.log(obj)
        obj = obj[0]

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
    SELECT ?homeTeamName ?awayTeamName ?homeTeamScore ?awayTeamScore ?date

	WHERE{

		:${id} :homeTeam ?team1.
		?team1 :teamOf ?team1a.
		?team1a :hasName ?homeTeamName.

		:${id} :awayTeam ?team2.
		?team2 :teamOf ?team2a.
		?team2a :hasName ?awayTeamName.

		:${id} :homeTeamScore ?homeTeamScore.
		:${id} :awayTeamScore ?awayTeamScore.
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
    }
    `
    // 3157

    public static readonly get_players = (id: number) => `
    ${Query.header}
	SELECT  ?Name ?teamName ?role
    WHERE
    { :${id} 	  :hasPlayedAsFirstTeam  ?team1 .
        ?team1    :isPersona            ?Persons .
        ?Persons  :hasName              ?Name .
        ?team1    :isMember             ?Member .
        ?Member   :teamOf               ?teamObject .
        ?teamObject  :hasName           ?teamName .
        ?team1    :role                 ?role
    }
    ORDER BY ?teamName ?role
    `
}
