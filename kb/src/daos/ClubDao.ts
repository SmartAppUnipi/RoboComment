import * as Entities from '../entities'
import * as DB from '../db'
import * as Errors from '../errors'

export class ClubDao {

    public static get(id: number): Promise<any> {
        const db = DB.Ontologies.data

        return new Promise((resolve, reject) =>
            db.execute(DB.Query.get_club(id), (_success, club) => {
                club = DB.Ontologies.process(club)[0]

                club === undefined ?
                    reject(Errors.NON_EXISTENT('club')) : resolve(club)
            })
        )
    }

}
