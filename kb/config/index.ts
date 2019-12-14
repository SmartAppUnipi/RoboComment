import path from 'path'

export const BASE_DIR: string = path.resolve(__dirname, '..')

const DB_PATH: string  = path.resolve(BASE_DIR, `${process.env.NODE_ENV !== 'production' ? 'db/dev' : 'db/production'}`)
export const DB_USERS: string = path.resolve(DB_PATH + '/users.json')
export const KB: string = path.resolve(DB_PATH + '/kb.ttl')

export const PORT: number = process.env.NODE_ENV !== 'production' ? 5005 : 8080
