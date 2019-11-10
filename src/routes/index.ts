import { Router } from 'express'
import UserRouter from './User'

const router: Router = Router()

router.use('/users', UserRouter)

export default router
