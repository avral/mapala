import steem from 'steem'
import {Client} from 'steem-rpc'
import {ChainConfig, PrivateKey, TransactionBuilder} from 'esteem-lib'

// TODO Написать общий класс для работы со всеми блокчейнами 

let blockchains = {
	// Конфигурации для блокчейнов
	'golos': {
		wss: 'wss://ws.mapala.net',
		prefix: 'GLS',
		chainId: '782a3039b478c839e4cb0c941ff4eaeb7df40bdd68bd441afd444b9da763de12'
	},
	'steemit': {
		wss: 'wss://steemd.steemit.com',
		prefix: 'STM',
		chainId: '0000000000000000000000000000000000000000000000000000000000000000'
	}
}

class MapalaBlockchain {
	constructor(blockchain) {
		this.bc = blockchains[blockchain]

		if (window.Api !== undefined) {
			window.Api.close()
		}

		// esteem-lib conf
		window.Api = Client.get({url: blockchain.wss}, true)
		window.Api.initPromise.then(response => {
			ChainConfig.setChainId(blockchain.chain_id)
		})

		// steem-js conf
		steem.config.set('websocket', blockchain.wss)
		steem.config.set('address_prefix', blockchain.address_prefix)
		steem.config.set('chain_id', blockchain.chain_id)
	},
}

export default MapalaBlockchain
