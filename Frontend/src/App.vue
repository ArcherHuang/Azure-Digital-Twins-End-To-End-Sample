<template>
  <!-- <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
  </nav> -->
  <router-view/>
</template>
<script>

const axios = require('axios');
const { EventHubConsumerClient } = require('@azure/event-hubs');

export default {
  data() {
    return {
      // queryADT: 'https://adt3dquery.ashyriver-e2c40e3c.japaneast.azurecontainerapps.io/adt/query/statistics',
      queryADT: `https://${process.env.VUE_APP_QUERY_ADT_URL}/adt/query/statistics`,
    };
  },
  components: {

  },
  created() {
    this.receiveEventHubData();
  },
  mounted() {
  },
  methods: {
    async receiveEventHubData() {
      const connectionString = process.env.VUE_APP_EVENTHUB_CONNECTION_STRING;
      const eventHubName = process.env.VUE_APP_EVENTHUB_NAME;
      const consumerGroup = process.env.VUE_APP_CONSUMER_GROUP_NAME;
      console.log(`connectionString: ${connectionString}`);
      console.log(`eventHubName: ${eventHubName}`);
      console.log(`consumerGroup: ${consumerGroup}`);
      const consumerClient = new EventHubConsumerClient(
        consumerGroup,
        connectionString,
        eventHubName,
      );
      this.subscription = consumerClient.subscribe({
        processEvents: async (events, context) => {
          console.log(`\nevents: ${JSON.stringify(events)}`);
          // eslint-disable-next-line
          if (events[0]['body'].hasOwnProperty('status')) {
            console.log(`type: ${events[0].body.status.type}`);
            let status = -1;
            if (events[0].body.status.type === 'Error') {
              status = 2;
            } else if (events[0].body.status.type === 'inOperation') {
              status = 1;
            } else if (events[0].body.status.type === 'Idle') {
              status = 0;
            }
            this.$store.commit('setMachineStatus', {
              status,
            });
          }
          // eslint-disable-next-line
          if(events[0]['body'].hasOwnProperty('statistics')) {
            axios.get(this.queryADT)
              .then((response) => {
                console.log(`response_data_api: ${JSON.stringify(response.data)}`);
                this.$store.commit('setMachineStatistics', {
                  standardDeviation: response.data.statisticsStandardDeviation,
                  average: response.data.statisticsAverage,
                  uniformity: response.data.statisticsUniformity,
                  max: response.data.statisticsMax,
                  min: response.data.statisticsMin,
                  maxMin: response.data.statisticsMaxMin,
                });
              })
              .catch((error) => console.log(error));
            // statistics from EventHub - Start
            // this.$store.commit('setMachineStatistics', {
            //   standardDeviation: events[0].body.statistics.standardDeviation,
            //   average: events[0].body.statistics.average,
            //   uniformity: events[0].body.statistics.uniformity,
            //   max: events[0].body.statistics.max,
            //   min: events[0].body.statistics.min,
            //   maxMin: events[0].body.statistics.maxMin,
            // });
            // statistics from EventHub - End
          }
          await context.updateCheckpoint(events[events.length - 1]);
        },
      });
    },
  },
};
</script>
<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
