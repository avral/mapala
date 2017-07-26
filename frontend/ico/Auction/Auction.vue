<template>
    <!-- <el-tabs v-model="activeTab" v-if="mobile" class="aucstats" >
        <el-tab-pane label="Bitcoin" name="btc">
            <h4><sup v-html="stats.week.btc.icon"></sup>{{stats.week.btc.value}}</h4>
        </el-tab-pane>
        <el-tab-pane label="USD" name="usd">Config</el-tab-pane>
    </el-tabs> -->
    <!-- <div class="auc-block" v-else> -->
    <div class="auc-block" :class="{aucblMobile: mobile}">
        <h3>Аукцион</h3>
        <el-row type="flex" class="auc-cent" justify="center" :gutter="20">
            <el-col class="week-wraper" :span="8">
                <auction-stat :stat="stats.week.btc" :isBold="true"></auction-stat>
                <!-- <auction-stat :stat="stats.week.gbg"></auction-stat> -->
            </el-col>
            <el-col :span="8">
                <auction-stat :stat="stats.full.usd" :isBold="true"></auction-stat>
                <auction-stat v-if="$route.name == 'ico'" :stat="stats.full.tokens"></auction-stat>
            </el-col>
        </el-row>
        <router-link v-if="$route.name == 'ico'" :to="{name: 'auction'}">
            <el-button class="auc-btn">Аукцион</el-button>
        </router-link>
    </div>
</template>

<script>
import AuctionStat from './AuctionStat.vue'

export default {
    props: [
        'btc',
        'gbg',
        'usd',
        'tokens',
        'mobile'
    ],
    components: {AuctionStat},
    data () {
        return {
            stats: {
                week: {
                    btc: {
                        value: this.btc,
                        title: 'Поступления за неделю',
                        icon: '<i class="fa fa-btc" aria-hidden="true"></i>'
                    },
                    gbg: {
                        value: this.gbg,
                        icon: 'GBG',
                    }
                },
                full: {
                    usd: {
                        value: this.usd,
                        title: 'Всего',
                        icon: '<i class="fa fa-usd" aria-hidden="true"></i>',

                    },
                    tokens: {
                        value: 810000,
                        title: 'токены на распределение',
                    }
                }
            },
            activeTab: 'btc'

        }
    }
}
</script>

<style scoped>
h3 {
    font-size: 30px;
    color: #0a0a0a;
    font-weight: normal;
    margin-bottom: 0;
}
.auc-block {
    text-align: center;
    padding-bottom: 100px;
}
.auc-cent {
    padding-top: 65px;
}
.week-wraper {
    border-right: solid 1.4px #dddddd;
}
.auc-btn {
    border: solid 2.4px #f47999;
    border-radius: 10px;
    color: #00a3e5;
    font-size: 24px;
    width: 174px;
    height: 68px;
}
.el-row {
    margin-bottom: 85px;
}
.aucblMobile {
    padding-bottom: 10px;
}
</style>