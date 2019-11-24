import { Request, Response, Router, Express } from 'express'
import { BAD_REQUEST, CREATED, OK, NOT_FOUND } from 'http-status-codes'
import { UserDao } from '../daos'
import { ParamsDictionary } from 'express-serve-static-core'
import { Persona, Match } from '../entities'
import { DateTime } from 'luxon'
import { MatchDao } from '../daos/MatchDao'

// Init shared
const router = Router()

router.get('/:id', async (req, res) => {
    try {
        const { id } = req.params as ParamsDictionary

        const result = await MatchDao.get(Number(id))

        return res.status(OK).json(result)
    } catch (err) {
        console.error(err)
        return res.status(NOT_FOUND).json({
            error: err,
        })
    }
})

export default router
