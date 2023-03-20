const axios = require('axios');
if (process.env.NODE_ENV !== 'production') {
  require('dotenv').config();
}
const cors = require('cors');
const express = require('express')
const bodyParser = require('body-parser')

const adtService = require('./adtService.js');
const ADT_Host_Name = process.env.ADT_Host_Name || '';

const app = express();
const port = process.env.PORT || 80;
app.use(bodyParser.json());
app.use(cors());

app.get('/hello', async (req, res) => {
  res.send({
    result: 'ok',
  });
});

app.get('/adt/query/statistics', async (req, res) => {
  try {
    const { token } = await adtService.getToken();
    const requestBody = {
      "query": "SELECT * FROM DIGITALTWINS WHERE $dtId='FilmCheck01'"
    }
    const response = await axios.post(
      `https://${ADT_Host_Name}/query?api-version=2020-10-31`,
      requestBody,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    const statisticsStandardDeviation = response.data.value[0].statisticsStandardDeviation;
    const statisticsAverage = response.data.value[0].statisticsAverage;
    const statisticsUniformity = response.data.value[0].statisticsUniformity;
    const statisticsMax = response.data.value[0].statisticsMax;
    const statisticsMin = response.data.value[0].statisticsMin;
    const statisticsMaxMin = response.data.value[0].statisticsMaxMin;
    res.send({
      statisticsStandardDeviation,
      statisticsAverage,
      statisticsUniformity,
      statisticsMax,
      statisticsMin,
      statisticsMaxMin,
    });
  } catch (err) {
    console.log(`error: ${err}`)
    res.send({
      adtHostName: ADT_Host_Name,
      url: `https://${ADT_Host_Name}/query?api-version=2020-10-31`,
      error: err,
    });
  }
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}!`)
})