import * as Entities from '../entities'
import * as DB from '../db'
import * as Errors from '../errors'

export class CupDao {

    public static get(id: number): Promise<any> {
        const db = DB.Ontologies.data

        return new Promise((resolve, reject) =>
            db.execute(DB.Query.get_cup(id), (_success, league) => {
                league = DB.Ontologies.process(league)[0]

                league === undefined ?
                    reject(Errors.NON_EXISTENT('league')) : resolve(league)
            })
        )
    }

}
