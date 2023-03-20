'use strict'

const express = require('express');
const bodyParser = require('body-parser');
const db = require('./models');
const Log = db.Log;
const app = express();
const axios = require('axios');
const tokenService = require('./tokenService.js');
if (process.env.NODE_ENV !== 'production') {
  require('dotenv').config();
}
const port = process.env.PORT || 80;
const ExperimentName = process.env['EXPERIMENT_NAME'];
const TriggerMlEndpoint = process.env['TRIGGER_ML_ENDPOINT'];

app.use(bodyParser.json());

app.get('/token', async (req, res) => {
  try {
    const { token } = await tokenService.getToken();
    res.send({ status: 'success', message: '取得 token', token });
  } catch (err) {
    res.send({ status: 'error', error: err });
  }
})

app.post('/', async (req, res) => {
  try {
    console.log(`\nrequest_body: ${JSON.stringify(req.body[0])}`);
    if ('data' in req.body[0]) {
      if ('validationCode' in req.body[0].data) {
        console.log(`\nAzure EventGrid subscription successfully validated`);
        res.send({ validationResponse: req.body[0].data.validationCode });
      } else {
        if (req.body[0].data.url) {
          const fileName = req.body[0].data.url.split("/").pop();
          const extension = fileName.split(".").pop();
          console.log(`Extension: ${extension}`);
          const date = fileName.split('.')[0].replace('L', '');
          console.log(`fileName: ${fileName}`);
          console.log(`date: ${date}`);
          console.log(`\n1-${req.body[0].data.api}: ${req.body[0].data.url}`);
          if (extension === 'log') {
            if (req.body[0].data.api === 'PutBlob') {
              Log.create({
                  name: fileName,
                  date,
              }).then(() => {
                  res.send({ status: 'success', action: req.body[0].data.api, url: req.body[0].data.url });
              })
            } else if (req.body[0].data.api === 'DeleteBlob') {
              Log.findOne({
                  where: {
                    name: fileName,
                  }
              }).then((element) => {
                  element.destroy();
                  res.send({ status: 'success', action: req.body[0].data.api, url: req.body[0].data.url });
              })
            }
          } else if (extension === 'csv') {
            if (req.body[0].data.api === 'PutBlob') {
              const { token } = await tokenService.getToken();
              console.log(`tokenService: ${token}`);
              const requestBody = {
                ExperimentName,
                RunSource: 'SDK',
              }
              const response = await axios.post(
                TriggerMlEndpoint,
                requestBody,
                {
                  headers: {
                    Authorization: `Bearer ${token}`,
                  },
                }
              );
            }
          }
        } else {
          res.send({ status: 'success', url: 'No URL' });
        }
      }
    } else {
      res.send({ status: 'error', error: 'No Data Info' });
    }
  } catch (err) {
    res.send({ status: 'error', error: err });
  }
})

app.listen(port, () => {
  console.log(`\nApp listening on port ${port} !`);
})