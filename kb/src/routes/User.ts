import { Router } from 'express'
import { BAD_REQUEST, OK } from 'http-status-codes'
import { UserDao } from '../daos'
import { ParamsDictionary } from 'express-serve-static-core'

// Init shared
const router = Router()

router.post('/', (req, res) => {
  try {
    let { user } = req.body
    if (!user) {
      return res.status(BAD_REQUEST).json({
        error: 'user is missing in body',
      })
    }

    user = UserDao.add(user)
    delete user.password
    return res.status(OK).json(user)
  } catch (err) {
    console.error(err.message, err)
    return res.status(BAD_REQUEST).json({
      error: err.message,
    })
  }
})

router.post('/login', (req, res) => {
  try {
    let { user } = req.body
    if (!user) {
      return res.status(BAD_REQUEST).json({
        error: 'user is missing in body',
      })
    }
    user = UserDao.login(user.email, user.password)
    delete user.password
    return res.status(OK).json(user)
  } catch (err) {
    console.error(err.message, err)
    return res.status(BAD_REQUEST).json({
      error: err.message,
    })
  }
})

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
    return res.status(BAD_REQUEST).json({
      error: err.message,
    })
  }
})

router.delete('/:email', (req, res) => {
  try {
    const { email } = req.params as ParamsDictionary
    UserDao.delete(email)
    return res.status(OK).end()
  } catch (err) {
    return res.status(BAD_REQUEST).json({
      error: err.message,
    })
  }
})

export default router
