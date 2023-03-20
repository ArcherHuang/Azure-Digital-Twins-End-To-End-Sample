<template>
  <transition name="modal">
    <div class="modal-history" v-if="showModal">
      <div class="modal-wrapper" @click.self="close" @keyup.enter="close">
        <div class="modal-container">
          <div class="modal-body">
            <template v-if="from =='log'">
              <div class="title">Log 資訊</div>
              <div v-if="!infos.length">目前尚無 Log</div>
              <table v-else class="table mt-3 table-hover">
                <thead class="thead-dark">
                  <tr>
                    <th scope="col">
                        Date
                    </th>
                    <th scope="col">
                        Name
                    </th>
                    <th scope="col">
                        File
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(element, index) in infos" :key="index">
                    <td class="pt-3">{{ element.date }}</td>
                    <td class="pt-3">{{ element.name }}</td>
                    <td class="pt-3">
                      <!-- <a :href="'https://adt3dstorageaccount.blob.core.windows.net/adt/Log/' + element.name" download>
                        下載
                      </a> -->
                      <a :href="'https://' + this.blobName + '.blob.core.windows.net/adt/Log/' + element.name" download>
                        下載
                      </a>
                    </td>
                  </tr>
                </tbody>
              </table>
            </template>
            <template v-else-if="from =='report'">
                <div class="title">Report 資訊</div>
                <div v-if="!infos.length">目前尚無 Report</div>
                <table v-else class="table mt-3 table-hover">
                <thead class="thead-dark">
                  <tr>
                    <th scope="col">
                        Date Time
                    </th>
                    <th scope="col">
                        Standard Deviation
                    </th>
                    <th scope="col">
                        Average
                    </th>
                    <th scope="col">
                        Uniformity
                    </th>
                    <th scope="col">
                        Max
                    </th>
                    <th scope="col">
                        Min
                    </th>
                    <th scope="col">
                        Max Min
                    </th>
                    <th scope="col">
                        Excel
                    </th>
                    <th scope="col">
                        Img
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(element, index) in infos" :key="index">
                    <td class="pt-3">{{ element.date }}</td>
                    <td class="pt-3">{{ element.standard_deviation }}</td>
                    <td class="pt-3">{{ element.average }}</td>
                    <td class="pt-3">{{ element.uniformity }}</td>
                    <td class="pt-3">{{ element.max }}</td>
                    <td class="pt-3">{{ element.min }}</td>
                    <td class="pt-3">{{ element.max_min }}</td>
                    <td class="pt-3">
                      <!-- <a :href="'https://adt3dstorageaccount.blob.core.windows.net/adt/Report/' + element.file_name" download>
                        下載
                      </a> -->
                      <a :href="'https://' + this.blobName + '.blob.core.windows.net/adt/Report/' + element.file_name" download>
                        下載
                      </a>
                    </td>
                    <td class="pt-3">
                      <!-- <a :href="'https://adt3dstorageaccount.blob.core.windows.net/adt/Report/' + element.file_name" download>
                        下載
                      </a> -->
                      <a :href="'https://' + this.blobName + '.blob.core.windows.net/adt/Report/' + element.file_name" download>
                        下載
                      </a>
                    </td>
                  </tr>
                </tbody>
              </table>
            </template>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>

export default {
  data() {
    return {
      blobName: process.env.VUE_APP_BLOB_NAME,
    };
  },
  props: {
    infos: {
      type: Array,
    },
    from: {
      type: String,
    },
  },
  created() {
  },
  mounted() {
  },
  computed: {
    showModal: {
      get() {
        return this.$store.state.showModal;
      },
      set(value) {
        this.$store.commit('setshowModal', value);
      },
    },
  },
  methods: {
    close() {
      this.showModal = false;
      this.$emit('after-submit');
    },
  },
};
</script>

<style scoped lang='scss'>
td:last-child {
  // background-color: #5696c7;
  width: 270px;
}

.table > thead > tr > th, .table > tbody > tr > td {
  vertical-align: middle;
}
.title {
  font-size: 25px;
}

a {
  color: black;
}

a:hover {
  text-decoration: none;
}
.date {
  width: 500px;;
}

.icon {
  color: gray;
  /* font-size: 3em; */
}
.modal-history {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.65);
  display: table;
  transition: opacity 0.3s ease;
}
.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}
.modal-container {
  // width: 852px;
  width: 882px;
  margin: 0px auto;
  padding: 10px 30px;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  font-family: Helvetica, Arial, sans-serif;
  overflow-y: auto;
  max-height: 600px;
}
.modal-body {
  color: black;
  margin: 20px 0;
}
.modal-enter {
  opacity: 0;
}
.modal-leave-active {
  opacity: 0;
}
.modal-enter .modal-container,
.modal-leave-active .modal-container {
  transform: scale(1.1);
}
</style>
