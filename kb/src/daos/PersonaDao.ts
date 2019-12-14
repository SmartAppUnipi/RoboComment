import * as Entities from '../entities'
import * as DB from '../db'
import * as Errors from '../errors'

export class PersonaDao {

    public static get(id: number): Promise<any> {
        const db = DB.Ontologies.data

        return new Promise((resolve, reject) =>
            db.execute(DB.Query.get_persona(id), (_success, persona) => {
                persona = DB.Ontologies.process(persona)[0]

                persona === undefined ?
                    reject(Errors.NON_EXISTENT('persona')) : resolve(persona)
            })
        )
    }

}
