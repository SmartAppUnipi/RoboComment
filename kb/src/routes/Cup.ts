import { Request, Response, Router, Express } from 'express'
import { BAD_REQUEST, CREATED, OK, NOT_FOUND } from 'http-status-codes'
import { UserDao } from '../daos'
import { ParamsDictionary } from 'express-serve-static-core'
import { Cup } from '../entities'
import { CupDao } from '../daos/CupDao'

// Init shared
const router = Router()

router.get('/:id/', async (req, res) => {
    try {
        const { id } = req.params as ParamsDictionary

        const result = await CupDao.get(Number(id))

        return res.status(OK).json(result)
    } catch (err) {
        console.error(err)
        return res.status(NOT_FOUND).json({
            error: err,
        })
    }
})

export default router
