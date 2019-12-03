import * as Entities from '../entities'
import * as DB from '../db'
import * as Errors from '../errors'

export class UserDao {

  public static login(email: string, pwd: string): Entities.User {
    const db = DB.Users.data

    const user = db.users.find(user => user.email === email && user.password === pwd)

    if (user === undefined) {
      throw Error(Errors.USER_NOT_FOUND)
    }

    return { ...user }
  }

  public static add(user: Entities.User): Entities.User {
    const db = DB.Users.data

    if (db.users.some(value => value.email === user.email)) {
      throw Error(Errors.EMAIL_ALREADY_USED)
    }

    user.id = db.users.length + 1
    db.users.push(user)

    DB.Users.save_db()
    return { ...user }
  }

  public static update(user: Entities.User): void {
    const db = DB.Users.data

    const i = db.users.findIndex(old_user => old_user.id === user.id)
    const old_user = db.users[i]

    if (old_user === undefined) {
      throw Error(Errors.USER_NOT_FOUND)
    }

    if (old_user === undefined) {
      throw Error(Errors.USER_NOT_FOUND)
    }

    db.users[i] = { ...user, password: old_user.password } as Entities.User

    DB.Users.save_db()
  }

  public static delete(email: string): void {
    const db = DB.Users.data

    db.users = db.users.filter(user => user.email !== email)
    console.log(db.users)
    DB.Users.save_db()
  }
}
