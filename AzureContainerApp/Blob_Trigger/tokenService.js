const { DefaultAzureCredential } = require("@azure/identity");
const credential = new DefaultAzureCredential();

const tokenService = {
  getToken: async (req, res) => {
    try {
      let { token } = await credential.getToken(
        'https://management.azure.com/.default'
      );
      return { status: "success", message: "成功取得 Token", token };
    } catch (err) {
      console.log(`Err: ${err}`);
      return { status: "error", message: "無法取得 Token" };
    }
  },
}

module.exports = tokenService;