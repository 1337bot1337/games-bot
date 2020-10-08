import express from 'express'
import cors from 'cors'

const app = express()
const PORT = process.env.PORT

app.use(cors())
app.use(express.json())

app.listen(PORT, () => console.log(`API started on port ${PORT}`))

export default app
