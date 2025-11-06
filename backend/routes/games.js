const express = require('express');
const router = express.Router();
const { requireAuth } = require('../middleware/auth');
const { listUserGames, addUserGame, updateProgress } = require('../controllers/gameController');

router.get('/', requireAuth, listUserGames);
router.post('/', requireAuth, addUserGame);
router.put('/:id/progress', requireAuth, updateProgress);

module.exports = router;