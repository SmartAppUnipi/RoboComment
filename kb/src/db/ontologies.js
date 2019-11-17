// const rdf = require('rdfstore')
// const fs = require('fs')

// // function _build() {
// //     await
// //     const rdf = fs.readFileSync('syntax.ttl').toString()
// // }

// // class Ontologies {
// //     static db = 
// // }

// class Ontologies {
//     static db = null
// }


// new rdf.Store((err, store) => {
//     const rdf = fs.readFileSync('syntax.ttl').toString()
//     store.load('text/turtle', rdf, (s, d) => {
//         store.registerDefaultProfileNamespaces()
//         store.setPrefix("rb", "http://www.semanticweb.org/dvara/ontologies/RoboComment#")
//         store.execute(`PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
//         PREFIX owl: <http://www.w3.org/2002/07/owl#>
//         PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
//         PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
//         PREFIX : <http://www.semanticweb.org/dvara/ontologies/RoboComment#>
//         SELECT ?name
//         WHERE { 
//          ?Persona :wasBornIn ?name.
//         }`, (success, results) => { console.log(success, results) })
//     })
// })

// // const rdf = require('rdflib')

// // const store = rdf.graph()
// // const me = store.sym("file:///home/danilo/Documents/SA/RoboComment/kb/src/db/RoboComment.owl")
// // const profile = me.doc()
// // const RB = new rdf.Namespace('http://www.semanticweb.org/dvara/ontologies/RoboComment#');
