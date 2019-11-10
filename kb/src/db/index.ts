import jsonfile from 'jsonfile'
import { User } from '../entities'

type DB = {
    users: User[]
}

export class Users {
    private static readonly db_file_path = 'src/db/users.json'
    public static readonly data: DB = jsonfile.readFileSync(Users.db_file_path)

    public static save_db(): Promise<any> {
        return jsonfile.writeFile(Users.db_file_path, Users.data, {
            spaces: 4
        })
    }
}
