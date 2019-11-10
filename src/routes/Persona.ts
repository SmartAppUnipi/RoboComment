import { Request, Response, Router, Express } from 'express'
import { BAD_REQUEST, CREATED, OK } from 'http-status-codes'
import { UserDao } from '../daos'
import { ParamsDictionary } from 'express-serve-static-core'
import { Persona } from 'src/entities'
import { DateTime } from 'luxon'

// Init shared
const router = Router()

const placeholder: Persona[] = [{
    id: 5,
    first_name: 'Andrea',
    last_name: 'Pirlo',
    date_of_birth: DateTime.fromObject({
        day: 22,
        month: 12,
        year: 1970
    }),
    career: [
        {
            year: '2003-2004',
            roles: [{
                type: 'player',
                shirt_number: 21,
                at: {
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
            }]
        }
    ]
}]

router.get('/:id', (req, res) => {
    try {
        const { id } = req.params as ParamsDictionary

        return res
            .status(OK)
            .type('json')
            .json(placeholder)
    } catch (err) {
        // logger.error(err.message, err);
        return res.status(BAD_REQUEST).json({
            error: err.message,
        })
    }
})
export default router
