const { prisma } = require('../utils/prisma');

async function listUserGames(req, res) {
  const userId = req.userId;
  const userGames = await prisma.userGame.findMany({ where: { userId }, include: { game: true } });
  res.json(userGames);
}

async function addUserGame(req, res) {
  const userId = req.userId;
  const { gameId, difficulty } = req.body;
  try {
    const userGame = await prisma.userGame.create({ data: { userId, gameId, difficulty } });
    res.status(201).json(userGame);
  } catch (err) {
    res.status(400).json({ error: 'Failed to add game', details: err.message });
  }
}

async function updateProgress(req, res) {
  const userId = req.userId;
  const id = Number(req.params.id);
  const { progress, totalPlaytime, currentQuestId } = req.body;
  const updated = await prisma.userGame.updateMany({
    where: { id, userId },
    data: { progress, totalPlaytime, currentQuestId }
  });
  if (updated.count === 0) return res.status(404).json({ error: 'Not found' });
  res.json({ ok: true });
}

module.exports = { listUserGames, addUserGame, updateProgress };