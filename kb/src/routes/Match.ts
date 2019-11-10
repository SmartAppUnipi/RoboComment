import { Request, Response, Router, Express } from 'express'
import { BAD_REQUEST, CREATED, OK } from 'http-status-codes'
import { UserDao } from '../daos'
import { ParamsDictionary } from 'express-serve-static-core'
import { Persona, Match } from '../entities'
import { DateTime } from 'luxon'

// Init shared
const router = Router()

const placeholder: Match[] = [{
    home: {
        name: 'JUV',
        city: 'Turin',
        palmares: [],
        stadium: {
            name: 'Nameless',
            capacity: 10000
        }
    },
    away: {
        name: 'LEC',
        city: 'Lecce',
        palmares: [],
        stadium: {
            name: 'Nameless',
            capacity: 30000
        }
    },
    result: [0, 0],
    date: DateTime.fromISO('2004-05-08'),
    home_team: [],
    away_team: []
}]

router.get('/:home/:away/:date', (req, res) => {
    try {
        const { home, away, date } = req.params as ParamsDictionary

        return res.status(OK).json(placeholder)
    } catch (err) {
        // logger.error(err.message, err);
        return res.status(BAD_REQUEST).json({
            error: err.message,
        })
    }
})

export default router
