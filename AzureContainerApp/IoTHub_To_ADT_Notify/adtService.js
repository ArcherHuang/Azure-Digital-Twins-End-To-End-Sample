const { DefaultAzureCredential } = require("@azure/identity");
const credential = new DefaultAzureCredential();

const adtService = {
  getToken: async (req, res) => {
    try {
      let { token } = await credential.getToken(
        'https://digitaltwins.azure.net/.default'
      );
      return { status: "success", message: "成功取得 Token", token };
    } catch (err) {
      console.log(`Err: ${err}`);
      return { status: "error", message: "無法取得 Token" };
    }
  },
}

module.exports = adtService;