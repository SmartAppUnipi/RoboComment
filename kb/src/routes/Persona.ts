import { Request, Response, Router, Express } from 'express'
import { BAD_REQUEST, CREATED, OK, NOT_FOUND } from 'http-status-codes'
import { UserDao } from '../daos'
import { ParamsDictionary } from 'express-serve-static-core'
import { Persona } from '../entities'
import { DateTime } from 'luxon'
import { Ontologies, Query } from '../db'
import { PersonaDao } from '../daos/PersonaDao'

// Init shared
const router = Router()

router.get('/:id', async (req, res) => {
    try {
        const { id } = req.params as ParamsDictionary

        const result = await PersonaDao.get(Number(id))

        return res
            .status(OK)
            .type('json')
            .json(result)
    } catch (err) {
        console.error(err)
        return res.status(NOT_FOUND).json({
            error: err,
        })
    }
})
export default router
