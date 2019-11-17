import * as Entities from '../entities'
import * as DB from '../db'
import * as Errors from '../errors'

export class ClubDao {

    public static get(id: number): Promise<any> {
        const db = DB.Ontologies.data

        return new Promise(resolve =>
            db.execute(DB.Query.get_club(id), (_success, results) => resolve(DB.Ontologies.process(results)))
        )
    }

}