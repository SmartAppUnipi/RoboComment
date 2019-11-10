import { Request, Response, Router, Express } from 'express'
import { BAD_REQUEST, CREATED, OK } from 'http-status-codes'
import { UserDao } from '../daos'
import { ParamsDictionary } from 'express-serve-static-core'
import { Club } from '../entities'

// Init shared
const router = Router()

const placeholder: Club = {
    name: 'ACM',
    city: 'Milan',
    palmares: [{
        name: 'UCL',
        year: '2003-2004'
    }],
    stadium: {
        name: 'San Siro',
        capacity: 70000
    }
}

router.get('/:id', (req, res) => {
    try {
        const { id } = req.params as ParamsDictionary

        return res.status(OK).json(placeholder)
    } catch (err) {
        // logger.error(err.message, err);
        return res.status(BAD_REQUEST).json({
            error: err.message,
        })
    }
})

export default router
