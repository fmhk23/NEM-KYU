var nem = require("nem-sdk").default;
var exec = require('child_process').exec;

var node_url = "http://104.128.226.60";
//var node_url = "http://127.0.0.1";

var endpoint = nem.model.objects.create("endpoint")(node_url, nem.model.nodes.websocketPort);

// Adress to subscribe

var address = "TCJ2QE7WZQLYWAF5EKEY2H3T57A2NP54W7HBSN5L";

var connector = nem.com.websockets.connector.create(endpoint, address);

connect(connector);

function connect(connector){
  return connector.connect().then(function() {
    nem.com.websockets.subscribe.account.transactions.confirmed(connector, function(res) {
      console.log(res);
      if (res.transaction.mosaics === undefined ) {
        console.log("mosaic undefined!");
        return;
      } else {
        console.log("mosaics have come!");
        var signer = res.transaction.signer;
        var address = nem.model.address.toAddress(signer, -104)
        var num = res.transaction.mosaics.length;
        for (var i = 0; i < num; i++){
          var namespace = res.transaction.mosaics[i].mosaicId.namespaceId;
          var name = res.transaction.mosaics[i].mosaicId.name;
          var message = nem.utils.format.hexToUtf8(res.transaction.message.payload);

          if ( namespace === 'company_a' & name === 'holiday2018'){
            command = 'python update_calendar.py ' + message;
            console.log(command);
            const exec = require('child_process').exec;
            exec(command ,(err, stdout, stderr) => {
              if(err){console.log(err);}
              console.log(stdout);
            });
            return;
          } else{
            console.log(namespace);
            console.log(name);
            return;
          }
        }
      }

    })
  })
}

