import express from 'express'
import BaseRouter from './routes'
import { OK } from 'http-status-codes'

export const app = express()

app.use(express.json())
app.use('/', BaseRouter)
app.get('/', (req, res) => {
    return res.status(OK).json({ hello: 'from the KB team!' })
})
