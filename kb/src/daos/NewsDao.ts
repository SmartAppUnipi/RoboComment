import * as Entities from '../entities'
import * as DB from '../db'
import * as Errors from '../errors'

export class NewsDao {

    public static get(id: number): Promise<any> {
        const db = DB.Ontologies.data

        return new Promise((resolve, reject) =>
            db.execute(DB.Query.get_news(id), (_success, news) => {
                news = DB.Ontologies.process(news)[0]

                news === undefined ?
                    reject(Errors.NON_EXISTENT('news')) : resolve(news)
            })
        )
    }

}
