import { Organization, Club } from './Club'
import { DateTime } from 'luxon'

type Role = {
    type: 'trainer' | 'player' | 'referee'
    at: Organization | Club
    shirt_number?: number
}

type Season = {
    year: string
    roles: Role[]
}

export interface Persona {
    id: number
    first_name: string
    last_name: string
    date_of_birth: DateTime
    career: Season[]
}
