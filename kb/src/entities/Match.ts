import { Club } from './Club'
import { DateTime } from 'luxon'
import { Persona } from './Persona'

type Result = [number, number]

export interface Match {
    home: Club
    away: Club
    result: Result
    date: DateTime
    home_team: Persona[],
    away_team: Persona[]
}
