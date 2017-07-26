<template>
    <div v-if="ico" class="icoInvest">
        <ico-stats :sections="sections"></ico-stats>
        <h1>История инвестиций</h1>
        <!-- <invest-table :table-data="ico.data_provider.allModels"></invest-table> -->
        <invest-table :table-data="investors"></invest-table>
    </div>
</template>

<script>
    import Chart from './Chart.vue'
    import IcoStats from './IcoStats.vue'
    import Auction from './Auction/Auction.vue'
    import AuctionInfo from './Auction/AuctionInfo.vue'
    import Faq from './Faq.vue'
    import InvestTable from './Investors/InvestTable.vue'
    import api from '../api'

    export default {
        components: {
            Chart,
            IcoStats,
            Auction,
            Faq,
            InvestTable
        },
        data () {
            return {
                investors: null
            }
        },
        computed: {
            ico: function () {
              return this.$parent.ico
            },
            sections: function () {
                var sections = [
                    {
                        title: 'инвестиции',
                        value: this.$parent.ico.total_btc.toFixed(6) + ' BTC'
                    },
                    {
                        title: 'распределенные токены',
                        value: this.$parent.ico.total_tokens.toFixed() + ' MPL'
                    },
                ]
                // console.log(this.ico.investors)
                return sections
            }
        },
        created () {
            // this.error = this.ico = null
            let that = this
            api.ico.investors(function(data) {
                // console.log(data)
                that.investors = data.data_provider.allModels
            });
        }
    }
</script>

<style scoped>
    h1 {
        margin-top: 130px;
    }
    .icoInvest {
        margin-top: -30px;
    }
</style>