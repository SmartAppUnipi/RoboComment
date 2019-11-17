import { app } from './server'
import { PORT, KB } from '../config'
import { Ontologies } from './db'

function create_store(): Promise<any> {
    const $rdf = require('rdfstore')
    const fs = require('fs')

    return new Promise(resolve => {
        // tslint:disable-next-line
        new $rdf.Store((_err: any, s: any) => {
            const rdf = fs.readFileSync(KB).toString()
            s.load('text/turtle', rdf, () => {
                s.registerDefaultProfileNamespaces()
                s.setPrefix('rb', 'http://www.semanticweb.org/dvara/ontologies/RoboComment#')
                resolve(s)
            })
        })
    })
}

function init(): Promise<boolean> {
    return new Promise(async resolve => {
        await create_store().then(store => (Ontologies.data as any) = store)
        resolve(true)
    })
}

init()
    .then(() =>
        app.listen(PORT, () =>
            console.log(`Express server started at http://127.0.0.1:${PORT}\n`)
        )
    )
