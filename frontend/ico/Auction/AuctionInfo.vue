<template>
    <div v-if="mobile" style="padding-top: 40px" class="walletMobile">
        <h3>Персональный BTC-адрес:</h3>
        <h4>{{btcAddress}}</h4>
        <el-tabs v-model="activeTab" v-if="this.wallet">
            <el-tab-pane label="BTC" name="btc">
                <h2><span>Инвестиции:</span> {{wallet.personal_btc}} BTC</h2>
            </el-tab-pane>
            <el-tab-pane label="GBG" name="gbg">
                <h2><span>Инвестиции:</span> {{wallet.personal_gbg}} GBG</h2>
            </el-tab-pane>
            <el-tab-pane label="Токены" name="tokens">
                <h2><span>Токены:</span> {{wallet.personal_tokens}} Mpl</h2>
            </el-tab-pane>
            <el-tab-pane label="Баунти" name="bounty">
                <h2><span>Баунти:</span> {{wallet.personal_bounty}} Mpl</h2>
            </el-tab-pane>
            <el-tab-pane label="USD" name="usd">
                <h2><span>Total USD:</span> {{wallet.total_personal_usd}} Mpl</h2>
            </el-tab-pane>
        </el-tabs>
    </div>
    <div v-else>
        <el-row type="flex" class="auc-row" justify="center" :gutter="20">
            <el-col :span="8">
                <el-card class="info-card big-card">
                    <h3>Персональная информация</h3>
                    <div class="stats" v-if="this.wallet">
                        <div class="stat">
                            <h4>Инвестиции:</h4>
                            <span>{{wallet.personal_btc}} BTC</span>
                            <span>{{wallet.personal_gbg}} GBG</span>
                        </div>
                        <div class="stat">
                            <h4>Токены</h4>
                            <span>{{wallet.personal_tokens}} Mpl</span>
                        </div>
                        <div class="stat">
                            <h4>Баунти</h4>
                            <span>{{wallet.personal_bounty}} Mpl</span>
                        </div>
                        <div class="stat">
                            <h4>Total USD</h4>
                            <span>{{wallet.total_personal_usd}} $</span>
                        </div>
                    </div>
                </el-card>
            </el-col>
            <el-col :span="8">
                <el-card v-for="card in cards" class="info-card small-card" :key=card.id v-if="btcAddress">
                    <h3>{{card.title}}</h3>
                    <span>{{card.body}}</span>
                    <p><a href="javascript:void(0)" @click="showHowTo(card)">инструкция</a></p>
                </el-card>
            </el-col>
            <el-dialog
              :title="howTo.title"
              :visible.sync="howTo.show"
              size="small">
                <how-to :items="howTo.insructions">
                  <template slot="item" scope="props">
                    <!-- <li :v-html="props.text"></li> -->
                    <li>{{ props.text }}</li>
                  </template>
                </how-to>
            </el-dialog>
        </el-row>
    </div>
</template>

<script>
import howTo from './HowTo.vue'
import api from '../../api'
import auth from '../../auth'

export default {
    components: {howTo},
    props: ["btcAddress", 'mobile'],
    data () {
        return {
            wallet: null,
            cards: [
                // {
                //     title: 'GBG аккаунт',
                //     body: 'mapala.ico',
                //     howTo: 'GBG',
                //     insructions: [
                //         'Для инвестиции в Золотых вам необходимо зайти в ваш кошелёк на Голосе и выбрать меню —> Передать',
                //         'Введите аккаунт mapala.ico, укажите желаемую сумму и в поле Заметка укажите имя аккаунта на Mapala.net, на который вы хотите, чтобы зачислились токены от этого платежа',
                //         'Через несколько минут транзакция появится в вашем личном кабинете Mapala',
                //         'Весь наш внутренний учёт ведётся в биткоинах, поэтому при зачислении инвестиции GBG будут конвертированы по курсу 1 мг Золота/BTC'
                //     ]

                // },
                {
                    title: 'Персональный BTC-адрес',
                    body: this.btcAddress,
                    howTo: 'BTC',
                    insructions: [
                        'Отправьте желаемую сумму на этот биткоин-адрес: ' + this.btcAddress,
                        'После 3-х подтверждений мы зачислим ваши средства и они будут отображаться в личном кабинете. Обычно это занимает 30-40 минут',
                    ]
                }
            ],
            howTo: {
                show: false,
                title: null,
                insructions: null
            },
            activeTab: 'btc'
        }
    },
    created() {
      let that = this
      api.ico.wallet(auth.user.username, function(data) {
        that.wallet = data
      });
    },
    methods: {
        showHowTo (card) {
            this.howTo.show = true
            this.howTo.title = card.title
            this.howTo.insructions = card.insructions
        }
    }
}
</script>

<style scoped>
    .auc-row {
        padding-top: 110px;
    }
    .info-card {
        text-align: center;
        box-shadow: 0 19px 52.7px 12.4px rgba(0, 0, 0, 0.06);
    }
    .info-card h3 {
        color: #00a3e5;
        font-weight: normal;
        font-size: 18px;
    }
    .info-card h4,
    .walletMobile span {
        color: #f47999;
        font-weight: normal;
        font-size: 18px;
        margin-bottom: 5px;
    }
    .info-card span {
        display: block;
    }
    .big-card {
        height: 422px;
    }
    .small-card {
        height: 158px;
        padding-bottom: 5px;
        margin-bottom: 93px;
    }
    .small-card p {
        margin-bottom: 2px;
        text-align: right;
    }
    .small-card p > a {
        color: #f47999;
    }
    .el-card__body {
        padding-bottom: 0;
    }
</style>