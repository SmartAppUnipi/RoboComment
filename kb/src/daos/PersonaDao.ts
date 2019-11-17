import * as Entities from '../entities'
import * as DB from '../db'
import * as Errors from '../errors'

export class PersonaDao {

    public static get(id: number): Promise<any> {
        const db = DB.Ontologies.data

        return new Promise(resolve =>
            db.execute(DB.Query.query1, (success, results) => resolve(results))
        )
    }

}
