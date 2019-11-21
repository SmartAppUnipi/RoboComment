import * as Entities from '../entities'
import * as DB from '../db'
import * as Errors from '../errors'
import { DateTime } from 'luxon'

export class MatchDao {

    public static get(id: number): Promise<Entities.Match> {
        const db = DB.Ontologies.data

        return new Promise(resolve =>
            db.execute(DB.Query.get_match(id), (success, results) => {
                results = DB.Ontologies.process(results)[0]
                resolve({
                    home: {
                        id: results.team1,
                        name: results.home
                    },
                    away: {
                        id: results.team2,
                        name: results.away
                    },
                    result: [results.home_score, results.away_score],
                    home_team: [],
                    away_team: []
                } as Entities.Match)
            })
        )
    }

}
