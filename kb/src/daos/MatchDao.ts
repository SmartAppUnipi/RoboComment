import * as Entities from '../entities'
import * as DB from '../db'
import * as Errors from '../errors'
import { DateTime } from 'luxon'

export class MatchDao {

    public static get(id: number): Promise<Entities.Match> {
        const db = DB.Ontologies.data

        return new Promise((resolve, reject) =>
            db.execute(DB.Query.get_match(id), (_success, match) => {
                match = DB.Ontologies.process(match)[0]

                if (match === undefined) {
                    reject(Errors.NON_EXISTENT('match'))
                    return
                }

                db.execute(DB.Query.get_players(id), (_success, players: any[]) => {
                    players = DB.Ontologies.process(players)
                    resolve({
                        home: {
                            id: match.team1,
                            name: match.home
                        },
                        away: {
                            id: match.team2,
                            name: match.away
                        },
                        result: [match.home_score, match.away_score],
                        home_team: players.filter(p => p.club === match.team1),
                        away_team: players.filter(p => p.club === match.team2)
                    } as Entities.Match)
                })
            })
        )
    }

}
