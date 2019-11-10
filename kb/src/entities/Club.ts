import { Cup } from './Cup'

export interface Organization {
    name: string
}

export interface Club extends Organization {
    palmares: Cup[]
    city: string
    stadium: Stadium
}

type Stadium = {
    name: string
    capacity: number
}
