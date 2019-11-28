import { Cup } from './Cup'

export interface Organization {
    id: number
    name: string
}

export interface Club extends Organization {
    city?: string
    stadium?: Stadium
}

type Stadium = {
    name: string
    capacity: number
}
