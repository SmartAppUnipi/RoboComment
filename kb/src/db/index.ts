import jsonfile from 'jsonfile'
import { User } from '../entities'
import { DB_USERS } from '../../config'

type DB = {
    users: User[]
}

export class Users {
    public static readonly data: DB = jsonfile.readFileSync(DB_USERS)

    public static save_db(): Promise<any> {
        return jsonfile.writeFile(DB_USERS, Users.data, {
            spaces: 4
        })
    }
}
