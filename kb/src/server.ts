import express from 'express'
import BaseRouter from './routes'
import logger from 'morgan'
import { OK } from 'http-status-codes'

export const app = express()
app.use(logger('dev'))
app.use(express.json())
app.use(express.urlencoded({extended: true}))
app.use('/', BaseRouter)

app.get('/', (req, res) => {
    return res.status(OK).json({ hello: 'from the KB team!' })
})
