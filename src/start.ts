import { app } from './server'

const port = Number(process.env.PORT || 3000)

app.listen(port, () =>
    console.log(`Express server started at http://127.0.0.1:${port}`)
)
