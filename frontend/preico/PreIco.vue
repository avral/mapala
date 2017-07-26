<template>
    <div id="app">
      <Top></Top>


      <iframe src="http://mapala.net/site/ico?user" frameborder="0">
      </iframe>

      <div v-on:click="iswitch" style="font-weight: bold;text-align: center;">
        Показать данные
      </div>
      <div v-if="show_info">

        <el-badge value="ico_data.amount" class="item">
          <el-button size="small">{{ico_data.amount}}</el-button>
        </el-badge> <br>

        <el-badge value="ico_data.bonuse_today" class="item">
          <el-button size="small">{{ico_data.bonuse_today}}</el-button>
        </el-badge> <br>

        <el-badge value="ico_data.btc_wallet" class="item">
          <el-button size="small">{{ico_data.btc_wallet}}</el-button>
        </el-badge> <br>

        <el-badge value="ico_data.current_rate" class="item">
          <el-button size="small">{{ico_data.current_rate}}</el-button>
        </el-badge> <br>

        <el-badge value="ico_data.data_provider" class="item">
          <el-button size="small">{{ico_data.data_provider}}</el-button>
        </el-badge> <br>

        <el-badge value="ico_data.interval" class="item">
          <el-button size="small">{{ico_data.interval}}</el-button>
        </el-badge> <br>

        <el-badge value="ico_data.personal_btc" class="item">
          <el-button size="small">{{ico_data.personal_btc}}</el-button>
        </el-badge> <br>

        <el-badge value="ico_data.personal_gbg" class="item">
          <el-button size="small">{{ico_data.personal_gbg}}</el-button>
        </el-badge> <br>

        <el-badge value="ico_data.tokens" class="item">
          <el-button size="small">{{ico_data.tokens}}</el-button>
        </el-badge> <br>

        <el-badge value="ico_data.total_btc" class="item">
          <el-button size="small">{{ico_data.total_btc}}</el-button>
        </el-badge> <br>

        <el-badge value="ico_data.total_tokens" class="item">
          <el-button size="small">{{ico_data.total_tokens}}</el-button>
        </el-badge> <br>

        <el-badge value="ico_data.total_usd" class="item">
          <el-button size="small">{{ico_data.total_usd}}</el-button>
        </el-badge> <br>

        <el-badge value="ico_data.weekly_btc" class="item">
          <el-button size="small">{{ico_data.weekly_btc}}</el-button>
        </el-badge> <br>

        <el-badge value="ico_data.weekly_gbg" class="item">
          <el-button size="small">{{ico_data.weekly_gbg}}</el-button>
        </el-badge> <br>

        <el-badge value="ico_data.xaxis" class="item">
          <el-button size="small">{{ico_data.xaxis}}</el-button>
        </el-badge> <br>

        <el-badge value="ico_data.yaxis" class="item">
          <el-button size="small">{{ico_data.yaxis}}</el-button>
        </el-badge> <br>


      </div>



    </div>
</template>

<script>
import Vue from 'vue'
import Top from '../base/Top.vue'
import auth from '../auth'


export default {
  name: 'PreIco',
  data () {
      return {
          ico_data: {
            amount:'',
            bonuse_today:'',
            btc_wallet:'',
            current_rate:'',
            data_provider:'',
            interval:'',
            personal_btc:'',
            personal_gbg:'',
            tokens:'',
            total_btc:'',
            total_tokens:'',
            total_usd:'',
            weekly_btc:'',
            weekly_gbg:'',
            xaxis:'',
            yaxis:'',
          },
          user: auth.user,
          show_info:false
      }
  },
  components:{
    'Top':Top
  },
  methods:{
    iswitch:function(){
      this.show_info=!this.show_info
    }
  },
  created(){
    console.log('GETTING ICO','http://mapala.net/api/v1/site/auction?callback=123&user=(username)'.replace('(username)',auth.user.username) )
    // console.log(this.$data.user.username)
    this.$http.jsonp('http://mapala.net/api/v1/site/auction?callback=123&user=(username)'.replace('(username)',this.$data.user.username), {}).then(function(data){
      // console.log(data)
      this.ico_data=data.data

    }, function(error) {
        // handle errors
        console.log(error,'EE')
    });

  }
}
</script>

<style scoped>
  iframe{
    width: 100%;
    height: 100%;
    min-height: 50vw;
    margin-top: -61px;
  }
  .item {
    margin-top: 10px;
    margin-right: 40px;
  }

</style>
