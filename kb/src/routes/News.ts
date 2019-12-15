import { Request, Response, Router, Express } from 'express'
import { BAD_REQUEST, CREATED, OK, NOT_FOUND } from 'http-status-codes'
import { ParamsDictionary } from 'express-serve-static-core'
import { NewsDao } from '../daos/NewsDao'

// Init shared
const router = Router()

router.get('/:id', async (req, res) => {
    try {
        const { id } = req.params as ParamsDictionary

        const result = await NewsDao.get(Number(id))

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
