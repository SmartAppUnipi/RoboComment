import { Request, Response, Router, Express } from 'express'
import { BAD_REQUEST, CREATED, OK } from 'http-status-codes'
import { UserDao } from '../daos'
import { ParamsDictionary } from 'express-serve-static-core'
import { Persona, Match } from '../entities'
import { DateTime } from 'luxon'
import { MatchDao } from '../daos/MatchDao'

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

router.get('/:id', async (req, res) => {
    try {
        const { id } = req.params as ParamsDictionary

        const result = await MatchDao.get(Number(id))

        return res.status(OK).json(result)
    } catch (err) {
        // logger.error(err.message, err);
        return res.status(BAD_REQUEST).json({
            error: err.message,
        })
    }
})

export default router
