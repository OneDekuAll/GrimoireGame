require('dotenv').config();
const express = require('express');
const { createServer } = require('http');
const cors = require('cors');
const { Server: IoServer } = require('socket.io');
const authRoutes = require('./routes/auth');
const gamesRoutes = require('./routes/games');
const { initPrisma } = require('./utils/prisma');

const PORT = process.env.PORT || 4000;
const app = express();
const server = createServer(app);
const io = new IoServer(server, { cors: { origin: '*' } });

app.use(cors());
app.use(express.json());

app.use('/api/auth', authRoutes);
app.use('/api/games', gamesRoutes);

app.get('/health', (_, res) => res.json({ ok: true }));

io.on('connection', socket => {
  console.log('socket connected:', socket.id);

  socket.on('gameplay:start', payload => {
    console.log('gameplay:start', payload);
    if (payload && payload.userId) socket.join(`user:${payload.userId}`);
    // TODO: persist session in DB
  });

  socket.on('hint:request', context => {
    console.log('hint:request', context);
    // TODO: integrate AI pipeline
    socket.emit('hint:ready', { hintText: 'This is a stub hint', hintLevel: 1 });
  });

  socket.on('disconnect', () => console.log('socket disconnected', socket.id));
});

async function main() {
  await initPrisma();
  server.listen(PORT, () => console.log(`Server running on port ${PORT}`));
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});