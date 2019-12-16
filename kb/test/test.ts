import newman from 'newman'
import fs from 'fs'
import jsonfile from 'jsonfile'
import { DB_USERS } from '../config'

const EmptyDB = {
  users: []
}

fs.writeFileSync(`${DB_USERS}.backup`, fs.readFileSync(DB_USERS))
jsonfile.writeFileSync(DB_USERS, EmptyDB, {
  spaces: 4
})

newman.run({
  collection: require('./tests.json'),
  reporters: 'cli'
})
