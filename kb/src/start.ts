import { app } from './server'
import { PORT } from '../config'

app.listen(PORT, () =>
    console.log(`Express server started at http://127.0.0.1:${PORT}\n`)
)
