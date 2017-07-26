<template>
    <div>
        <!-- <router-view name="top"></router-view> -->
        <router-view class="ico"></router-view>
        <!-- <chart :x="ico.xaxis" :y="ico.yaxis"></chart> -->
    </div>
</template>

<script>
    // import Chart from './Chart.vue'
    // import IcoStats from './IcoStats.vue'
    // import Auction from './Auction/Auction.vue'
    // import AuctionInfo from './Auction/AuctionInfo.vue'
    // import Faq from './Faq.vue'
    // import InvestTable from './Investors/InvestTable.vue'
  import auth from '../auth'

    import api from '../api'

    export default {
        // components: {
        //  Chart,
        //  IcoStats,
        //  Auction,
        //  Faq,
        //  InvestTable,
        //  AuctionInfo
        // },
        data () {
            return {
                title: 'ICO',
                ico: null,
                error: null,
            }
        },
        computed: {
          mobile () {
            return this.$store.state.mobile.mobile()
          }
        },
        methods: {
           //  fetchData () {
           //    this.error = this.ico = null
           //    let that = this
           //    api.ico.getData(function(data) {
                 //  that.ico = data
              // });
           //  }
        },
        beforeCreate () {
            this.error = this.ico = null
            let that = this
            api.ico.auction(auth.user.username, function(data) {
              // console.log(data)
              that.ico = data
            });
        },
        // mounted () {
        //  console.log(this.ico)
        // }
    }
</script>

<style>
  .ico {
    font-family: Roboto;
    overflow-x: hidden;
  }
  .el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
  .auc-bg {
    padding-top: 80px;
    padding-bottom: 100px;
  }
  .ico-bottom {
    text-align: center;
    padding-top: 40px;
    padding-bottom: 40px;
    font-size: 24px
  }
  .ico-bottom h4 {
    height: 127px;
    max-width: 200px;
    padding-left: 80px;
    padding-top: 40px;
    font-weight: normal;
  }
  .ico-bottom a {
    text-decoration: none;
  }
  .ico-hist {
    background: url('../assets/ico/history.png') no-repeat;
  }
  .ico-blog {
    background: url('../assets/ico/blog.png') no-repeat;
  }
  h1, h3 {
    font-weight: normal;
    text-align: center;
  }
</style>