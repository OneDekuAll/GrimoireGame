const express = require('express');
const router = express.Router();
const { pool } = require('../config/database');

router.get('/game/:gameId', async (req, res, next) => {
  try {
    const { type, difficulty } = req.query;
    
    let query = 'SELECT * FROM quests WHERE game_id = $1';
    const params = [req.params.gameId];
    let paramCount = 2;

    if (type) {
      query += ` AND quest_type = $${paramCount}`;
      params.push(type);
      paramCount++;
    }

    if (difficulty) {
      query += ` AND difficulty_rating <= $${paramCount}`;
      params.push(parseInt(difficulty));
      paramCount++;
    }

    query += ' ORDER BY quest_type, name';

    const result = await pool.query(query, params);
    res.json({ quests: result.rows });
  } catch (error) {
    next(error);
  }
});

router.get('/:id', async (req, res, next) => {
  try {
    const result = await pool.query(
      'SELECT * FROM quests WHERE id = $1',
      [req.params.id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Quest not found' });
    }

    res.json({ quest: result.rows[0] });
  } catch (error) {
    next(error);
  }
});

router.get('/user/progress', async (req, res, next) => {
  try {
    const { game_id, status } = req.query;
    
    let query = `
      SELECT uqp.*, q.name, q.description, q.quest_type, q.difficulty_rating, g.name as game_name
      FROM user_quest_progress uqp
      JOIN quests q ON uqp.quest_id = q.id
      JOIN games g ON q.game_id = g.id
      WHERE uqp.user_id = $1
    `;
    const params = [req.user.userId];
    let paramCount = 2;

    if (game_id) {
      query += ` AND q.game_id = $${paramCount}`;
      params.push(game_id);
      paramCount++;
    }

    if (status) {
      query += ` AND uqp.status = $${paramCount}`;
      params.push(status);
      paramCount++;
    }

    query += ' ORDER BY uqp.started_at DESC';

    const result = await pool.query(query, params);
    res.json({ progress: result.rows });
  } catch (error) {
    next(error);
  }
});

router.post('/:id/start', async (req, res, next) => {
  try {
    const questId = req.params.id;
    const userId = req.user.userId;

    const questCheck = await pool.query(
      'SELECT id, name FROM quests WHERE id = $1',
      [questId]
    );

    if (questCheck.rows.length === 0) {
      return res.status(404).json({ error: 'Quest not found' });
    }

    const result = await pool.query(
      `INSERT INTO user_quest_progress (user_id, quest_id, status, started_at)
       VALUES ($1, $2, 'in_progress', NOW())
       ON CONFLICT (user_id, quest_id) 
       DO UPDATE SET status = 'in_progress', started_at = NOW()
       RETURNING *`,
      [userId, questId]
    );

    res.json({
      message: 'Quest started',
      progress: result.rows[0],
      quest: questCheck.rows[0]
    });
  } catch (error) {
    next(error);
  }
});

router.put('/:id/progress', async (req, res, next) => {
  try {
    const { current_objective, status } = req.body;
    const questId = req.params.id;
    const userId = req.user.userId;

    const result = await pool.query(
      `UPDATE user_quest_progress 
       SET current_objective = COALESCE($1, current_objective),
           status = COALESCE($2, status),
           completed_at = CASE WHEN $2 = 'completed' THEN NOW() ELSE completed_at END
       WHERE user_id = $3 AND quest_id = $4
       RETURNING *`,
      [current_objective, status, userId, questId]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Quest progress not found' });
    }

    res.json({
      message: 'Progress updated',
      progress: result.rows[0]
    });
  } catch (error) {
    next(error);
  }
});

router.post('/:id/complete', async (req, res, next) => {
  try {
    const questId = req.params.id;
    const userId = req.user.userId;

    const progressResult = await pool.query(
      'SELECT started_at FROM user_quest_progress WHERE user_id = $1 AND quest_id = $2',
      [userId, questId]
    );

    if (progressResult.rows.length === 0) {
      return res.status(404).json({ error: 'Quest not started' });
    }

    const startTime = progressResult.rows[0].started_at;
    const completionTime = Math.floor((Date.now() - new Date(startTime).getTime()) / 60000); // minutes

    const result = await pool.query(
      `UPDATE user_quest_progress 
       SET status = 'completed',
           completed_at = NOW(),
           completion_time = $1
       WHERE user_id = $2 AND quest_id = $3
       RETURNING *`,
      [completionTime, userId, questId]
    );

    res.json({
      message: 'Quest completed! 🎉',
      progress: result.rows[0],
      completion_time_minutes: completionTime
    });
  } catch (error) {
    next(error);
  }
});

router.get('/:id/stats', async (req, res, next) => {
  try {
    const questId = req.params.id;

    const stats = await pool.query(
      `SELECT 
         COUNT(*) as total_attempts,
         COUNT(CASE WHEN status = 'completed' THEN 1 END) as completions,
         AVG(completion_time) FILTER (WHERE status = 'completed') as avg_completion_time,
         AVG(hints_used) as avg_hints_used
       FROM user_quest_progress
       WHERE quest_id = $1`,
      [questId]
    );

    res.json({ stats: stats.rows[0] });
  } catch (error) {
    next(error);
  }
});

router.post('/:id/abandon', async (req, res, next) => {
  try {
    const result = await pool.query(
      `UPDATE user_quest_progress 
       SET status = 'abandoned'
       WHERE user_id = $1 AND quest_id = $2
       RETURNING *`,
      [req.user.userId, req.params.id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Quest progress not found' });
    }

    res.json({
      message: 'Quest abandoned',
      progress: result.rows[0]
    });
  } catch (error) {
    next(error);
  }
});

module.exports = router;