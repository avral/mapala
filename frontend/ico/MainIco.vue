<template>
    <div v-if="ico" >
        <h3 v-if="mobile">Инвестируй в первое применение технологии блокчейн для путешественников</h3>
        <h1 v-else>Инвестируй в первое применение технологии блокчейн для путешественников</h1>
        <chart :x="ico.xaxis" :y="ico.yaxis"></chart>
        <ico-stats :sections="sections"></ico-stats>
        <el-row type="flex" class="auc-bg" justify="center" :gutter="20">
            <el-col :xs="24" :sm="24" :md="18" :lg="18">
                <el-card class="auc-card">
                    <auction  :mobile="mobile" :btc="ico.weekly_btc" :gbg="ico.weekly_gbg" :usd="ico.total_usd" :tokens="ico.total_tokens"></auction>
                </el-card>
            </el-col>
        </el-row>
        <el-row class="ico-bottom" type="flex" justify="center" :gutter="20">
            <el-col :xs="12" :sm="12" :md="6" :lg="6">
                <router-link :to="{name: 'investors'}">
                    <h4 class="ico-hist">История<br>Pre-ICO</h4>
                </router-link>
            </el-col>
            <el-col :xs="12" :sm="12" :md="6" :lg="6">
                <router-link to="/mapala">
                    <h4 class="ico-blog">Блог<br>Mapala</h4>
                </router-link>
            </el-col>
        </el-row>
        <faq></faq>
    </div>
</template>

<script>
    import Chart from './Chart.vue'
    import IcoStats from './IcoStats.vue'
    import Auction from './Auction/Auction.vue'
    import AuctionInfo from './Auction/AuctionInfo.vue'
    import Faq from './Faq.vue'
    import InvestTable from './Investors/InvestTable.vue'
    
    export default {
        components: {
            Chart,
            IcoStats,
            Auction,
            Faq,
        },
        data () {
            return {
                
            }
        },
        computed: {
            ico: function () {
              return this.$parent.ico
            },
            mobile () {
              return this.$store.state.mobile.mobile()
            },
            sections: function () {
                var sections = [
                    {
                        title: 'текущий курс',
                        value: this.$parent.ico.current_rate + ' BTC/MPL'
                    },
                    {
                        title: 'инвестиции',
                        value: this.$parent.ico.total_btc.toFixed(6) + ' BTC'
                    },
                    {
                        title: 'распределенные токены',
                        value: this.$parent.ico.total_tokens.toFixed() + ' MPL'
                    },
                ]

                return sections
            }
        },
        // created () {
        //  this.ico = this.$parent.ico
        //  console.log(this.ico)
        // },
        // watch: {
        //     // whenever question changes, this function will run
        //     question: function (newQuestion) {
        //       this.answer = 'Waiting for you to stop typing...'
        //       this.getAnswer()
        //     }
        //   },
    }
</script>

<style>
.auc-card {
    padding-top: 54px;
    padding-bottom: 66px;
    box-shadow: 0 15px 58.5px 6.5px rgba(0, 0, 0, 0.06);
    text-align: center;
}
</style>