import { Request, Response, Router, Express } from 'express'
import { BAD_REQUEST, CREATED, OK } from 'http-status-codes'
import { UserDao } from '../daos'
import { ParamsDictionary } from 'express-serve-static-core'

// Init shared
const router = Router()

/******************************************************************************
 *                      Get All Users - "GET /users/:id"
 ******************************************************************************/

router.get('/:id', (req, res) => {
    try {
        const { id } = req.params as ParamsDictionary
        const user = UserDao.get(Number(id))
        return res.status(OK).json(user)
    } catch (err) {
        // logger.error(err.message, err);
        return res.status(BAD_REQUEST).json({
            error: err.message,
        })
    }
})

/******************************************************************************
 *                       Add One - "POST /users/"
 ******************************************************************************/

router.post('/', (req, res) => {
    try {
        let { user } = req.body
        if (!user) {
            return res.status(BAD_REQUEST).json({
                error: 'user is missing in body',
            })
        }
        user = UserDao.add(user)
        return res.status(CREATED).json(user)
    } catch (err) {
        // logger.error(err.message, err)
        return res.status(BAD_REQUEST).json({
            error: err.message,
        })
    }
})

/******************************************************************************
 *                       Update One - "PUT /users/"
 ******************************************************************************/

router.put('/', (req, res) => {
    try {
        let { user } = req.body
        if (!user) {
            return res.status(BAD_REQUEST).json({
                error: 'user is missing in body',
            })
        }
        user = UserDao.update(user)
        return res.status(OK).json(user)
    } catch (err) {
        // logger.error(err.message, err)
        return res.status(BAD_REQUEST).json({
            error: err.message,
        })
    }
})

/******************************************************************************
 *                       Update One - "DELETE /users/"
 ******************************************************************************/

router.delete('/:id', (req, res) => {
    try {
        const { id } = req.params as ParamsDictionary
        const user = UserDao.delete(Number(id))
        return res.status(OK).end()
    } catch (err) {
        // logger.error(err.message, err);
        return res.status(BAD_REQUEST).json({
            error: err.message,
        })
    }
})

export default router
