type DB = {
    execute(query: string, callback: (success: any, results: any) => void): void
}
export class Ontologies {
    public static readonly data: DB
}

// tslint:disable-next-line: max-classes-per-file
export class Query {
    public static readonly query1: string = `
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX : <http://www.semanticweb.org/dvara/ontologies/RoboComment#>
    SELECT ?name
    WHERE {
     ?Persona :wasBornIn ?name.
    }
    `
}

// function create_store(): Promise<any> {
//     const $rdf = require('rdfstore')
//     return new Promise(resolve => {
//         new $rdf.Store((err: any, s: any) => {
//             const rdf = fs.readFileSync('syntax.ttl').toString()
//             s.load('text/turtle', rdf, () => {
//                 s.registerDefaultProfileNamespaces()
//                 s.setPrefix("rb", "http://www.semanticweb.org/dvara/ontologies/RoboComment#")
//                 resolve(s)
//             })
//         })
//     })
// }

// class Ontologies {
//     public static readonly db = {}
// }

// create_store()
//     .then(store => {
//         (Ontologies.db as any) = store
//         return store
//     })
//     .then((store) => store.execute(`PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
// PREFIX owl: <http://www.w3.org/2002/07/owl#>
// PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
// PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
// PREFIX : <http://www.semanticweb.org/dvara/ontologies/RoboComment#>
// SELECT ?name
// WHERE { 
//     ?Persona :wasBornIn ?name.
// }`, (success, results) => { console.log(success, results) }))
