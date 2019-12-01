import { app } from './server'
import { KB } from '../config'
import { Ontologies } from './db'
import jsonfile from 'jsonfile'

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

const host: string = jsonfile.readFileSync('../routes.json').qi
const PORT: number = Number((host.match(/\d\d\d\d/) as RegExpMatchArray)[0])
init()
  .then(() =>
    app.listen(PORT, () =>
      console.log(`Express server started at http://127.0.0.1:${PORT}\n`)
    )
  )
