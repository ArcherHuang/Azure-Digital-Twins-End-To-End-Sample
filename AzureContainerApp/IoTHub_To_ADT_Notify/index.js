const { EventHubConsumerClient } = require('@azure/event-hubs');
const axios = require('axios');
require('dotenv').config();

const db = require('./models');
const Report = db.Report;
const Status = db.Status;

const adtService = require('./adtService.js');

const ADT_Host_Name = process.env['ADT_Host_Name'];
const eventHubConnectionString = process.env['EVENTHUB_CONNECTION_STRING'] || '';
const eventHubName = process.env['EVENTHUB_NAME'] || '';
const consumerGroup = process.env['CONSUMER_GROUP_NAME'] || '';
const webhook_url = process.env['WEBHOOK_URL'] || '';
const title = 'FilmCheck AS300 警示訊息';

const consumerClient = new EventHubConsumerClient(
  consumerGroup,
  eventHubConnectionString,
  eventHubName
);

this.subscription = consumerClient.subscribe({
  processEvents: async (events, context) => {
    console.log(events);
    if (events.length > 0) {
      console.log(`events: ${JSON.stringify(events)}`);
      const oauthResponse = await adtService.getToken();
      let deviceID = events[0]['systemProperties']['iothub-connection-device-id']
      console.log(`deviceID: ${deviceID}`);
      let statusArray = [];
      let statisticsArray = [];
      let requestBody = [];
      let reportJSON = {};
      let statusJSON = {};
      if (events[0]['body'].hasOwnProperty('status')) {
        console.log(`status date: ${events[0]['body']['status']['date']}`);
        console.log(`status time: ${events[0]['body']['status']['time']}`);
        console.log(`status type: ${events[0]['body']['status']['type']}`);
        console.log(`status message: ${events[0]['body']['status']['message']}`);
        // -1 shutdown    , default color
        //  0 idle        , green color
        //  1 inOperation , orange color
        //  2 error       , red color
        let typeError = -1;
        if(events[0]['body']['status']['type'] === 'Idle') {
          typeError = 0;
        } else if(events[0]['body']['status']['type'] === 'inOperation') {
          typeError = 1;
        } else if(events[0]['body']['status']['type'] === 'Error') {
          typeError = 2;
          axios
            .post(webhook_url, {
              title,
              'text': `${events[0]['body']['status']['date']} ${events[0]['body']['status']['time']} ${events[0]['body']['status']['message']}`,
            })
            .then(res => {
              console.log(`statusCode: ${res.status}`);
              console.log(res);
            })
            .catch(error => {
              console.error(error);
            })
        }
        statusArray.push({
          op: "replace",
          path: '/statusDate',
          value: events[0]['body']['status']['date'],
        });
        statusArray.push({
          op: 'replace',
          path: '/statusTime',
          value: events[0]['body']['status']['time'],
        });
        statusArray.push({
          op: 'replace',
          path: '/typeError',
          value: typeError,
        });
        statusArray.push({
          op: 'replace',
          path: '/statusMessage',
          value: events[0]['body']['status']['message'],
        });
        statusJSON = {
          date: events[0]['body']['status']['date'],
          time: events[0]['body']['status']['time'],
          type: events[0]['body']['status']['type'],
          message: events[0]['body']['status']['message'],
        };
      }
      if(events[0]['body'].hasOwnProperty('statistics')) {
        console.log(`statistics date: ${events[0]['body']['statistics']['date']}`);
        console.log(`statistics time: ${events[0]['body']['statistics']['time']}`);
        console.log(`statistics standardDeviation: ${events[0]['body']['statistics']['standardDeviation']}`);
        console.log(`statistics average: ${events[0]['body']['statistics']['average']}`);
        console.log(`statistics uniformity: ${events[0]['body']['statistics']['uniformity']}`);
        console.log(`statistics max: ${events[0]['body']['statistics']['max']}`);
        console.log(`statistics min: ${events[0]['body']['statistics']['min']}`);
        console.log(`statistics maxMin: ${events[0]['body']['statistics']['maxMin']}`);
        statisticsArray.push({
          op: "replace",
          path: '/statisticsDate',
          value: events[0]['body']['statistics']['date'],
        });
        statisticsArray.push({
          op: "replace",
          path: '/statisticsTime',
          value: events[0]['body']['statistics']['time'],
        });
        statisticsArray.push({
          op: "replace",
          path: '/statisticsStandardDeviation',
          value: events[0]['body']['statistics']['standardDeviation'],
        });
        statisticsArray.push({
          op: "replace",
          path: '/statisticsAverage',
          value: events[0]['body']['statistics']['average'],
        });
        statisticsArray.push({
          op: "replace",
          path: '/statisticsUniformity',
          value: events[0]['body']['statistics']['uniformity'],
        });
        statisticsArray.push({
          op: "replace",
          path: '/statisticsMax',
          value: events[0]['body']['statistics']['max'],
        });
        statisticsArray.push({
          op: "replace",
          path: '/statisticsMin',
          value: events[0]['body']['statistics']['min'],
        });
        statisticsArray.push({
          op: "replace",
          path: '/statisticsMaxMin',
          value: events[0]['body']['statistics']['maxMin'],
        });
        reportJSON = {
          standard_deviation: events[0]['body']['statistics']['standardDeviation'],
          average: events[0]['body']['statistics']['average'],
          uniformity: events[0]['body']['statistics']['uniformity'],
          max: events[0]['body']['statistics']['max'],
          min: events[0]['body']['statistics']['min'],
          max_min: events[0]['body']['statistics']['maxMin'],
          file_name: events[0]['body']['statistics']['fileName'],
          date: events[0]['body']['statistics']['fileName'].split('.')[0],
        };
      }
      if(statusArray.length > 0) {
        requestBody.push(...statusArray)
      }
      if(statisticsArray.length > 0) {
        requestBody.push(...statisticsArray)
      }
      console.log(`requestBody: ${JSON.stringify(requestBody)}`);
      try {
        console.log(`\nurl: https://${ADT_Host_Name}/digitaltwins/${deviceID}?api-version=2020-10-31`);
        console.log(`token:Bearer ${oauthResponse.token}\n`);
        const response = await axios.patch(
          `https://${ADT_Host_Name}/digitaltwins/${deviceID}?api-version=2020-10-31`,
          requestBody,
          {
            headers: {
              Authorization: `Bearer ${oauthResponse.token}`,
            },
          }
        );
        // console.log(`Response: ${JSON.stringify(response)}`);
      } catch (err) {
        // console.error(err);
      }
      console.log(`reportJSON: ${JSON.stringify(reportJSON)}`);
      if (Object.keys(reportJSON).length !== 0) {
        Report.findOne({
          where: {
            file_name: events[0]['body']['statistics']['fileName'],
          }
        }).then((element) => {
          if (!element) {
            Report.create({
              standard_deviation: events[0]['body']['statistics']['standardDeviation'],
              average: events[0]['body']['statistics']['average'],
              uniformity: events[0]['body']['statistics']['uniformity'],
              max: events[0]['body']['statistics']['max'],
              min: events[0]['body']['statistics']['min'],
              max_min: events[0]['body']['statistics']['maxMin'],
              file_name: events[0]['body']['statistics']['fileName'],
              date: events[0]['body']['statistics']['fileName'].split('.')[0],
            }).then(() => {
                // console.log('Insert Finished.');
            })
          }
        })
      }
      if (Object.keys(statusJSON).length !== 0) {
        Status.findOne({
          where: {
            date: statusJSON.date,
            time: statusJSON.time,
          }
        }).then((element) => {
          if (!element) {
            Status.create(statusJSON).then(() => {
              // console.log('Insert Finished.');
            })
          }
        })
      }
    }
    await context.updateCheckpoint(events[events.length - 1]);
  },
});