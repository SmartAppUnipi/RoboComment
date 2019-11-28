import { Router } from 'express'
import UserRouter from './User'
import PersonaRouter from './Persona'
import MatchRouter from './Match'
import CupRouter from './Cup'
import ClubRouter from './Club'

const router: Router = Router()

router.use('/users', UserRouter)
router.use('/persona', PersonaRouter)
router.use('/match', MatchRouter)
router.use('/league', CupRouter)
router.use('/club', ClubRouter)

export default router
