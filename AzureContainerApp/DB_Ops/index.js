'use strict'

const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const db = require('./models');
const Log = db.Log;
const Report = db.Report;
const Status = db.Status;

const app = express();
if (process.env.NODE_ENV !== 'production') {
  require('dotenv').config();
}
const port = process.env.PORT || 80;

app.use(bodyParser.json());
app.use(cors());

// GET http://localhost/logs
// Response
// {
//     "status": "success",
//     "message": "取得所有 Log 清單",
//     "logs": [
//         {
//             "name": "L20230218.log",
//             "date": "20230218"
//         }
//     ]
// }

// GET http://localhost/logs
app.get('/logs', async (req, res) => {
  try {
    Log.findAll({
      attributes: ['name', 'date'],
    }).then(logs => {
      res.send({ status: 'success', message: '取得所有 Log 清單', infos: logs });
    })
  } catch (err) {
    res.send({ status: 'error', error: err });
  }
})

// GET http://localhost/status/latest
app.get('/status/latest', async (req, res) => {
  try {
    Status.findOne({
      attributes: [
        'date',
        'time',
        'type',
        'message',
      ],
      order: [[ 'createdAt', 'DESC' ]],
    }).then(logs => {
      res.send({ status: 'success', message: '取得最新一筆 status', infos: logs });
    })
  } catch (err) {
    res.send({ status: 'error', error: err });
  }
})

// GET http://localhost/reports/latest
app.get('/reports/latest', async (req, res) => {
  try {
    Report.findOne({
      attributes: [
        'standard_deviation',
        'average',
        'uniformity',
        'max',
        'min',
        'max_min',
      ],
      order: [[ 'createdAt', 'DESC' ]],
    }).then(reports => {
      res.send({ status: 'success', message: '取得最新一筆 Report', infos: reports });
    })
  } catch (err) {
    res.send({ status: 'error', error: err });
  }
})

app.get('/reports', async (req, res) => {
  try {
    Report.findAll({
      attributes: [
        'standard_deviation',
        'average',
        'uniformity',
        'max',
        'min',
        'max_min',
        'file_name',
        'date',
      ],
    }).then(reports => {
      res.send({ status: 'success', message: '取得所有 Report 清單', infos: reports });
    })
  } catch (err) {
    res.send({ status: 'error', error: err });
  }
})

app.listen(port, () => {
  console.log(`\nApp listening on port ${port} !`);
})