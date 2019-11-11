import newman from 'newman'
import fs from 'fs'
import jsonfile from 'jsonfile'
import { DB_USERS } from '../config'

const EmptyDB = {
    users: []
}

jsonfile.writeFileSync(DB_USERS, EmptyDB, {
    spaces: 4
})

newman.run({
    collection: require('./tests.json'),
    reporters: 'cli'
})
