const express = require('express');
const app = express();
const router = express.Router();

router.get('/', (req, res) => res.send('welcome'));


module.exports = router;