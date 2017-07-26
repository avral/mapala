<template>
    <el-row type="flex" class="auc-bg" justify="center" :gutter="20">
        <el-col :xs="24" :sm="24" :md="18" :lg="18">
            <data-tables
                :data="tableData"
                :search-def="{show: false}"
                :has-action-col="false"
                style="width: 100%"
                align="center"
                header-align="center">
                <el-table-column
                  prop="id"
                  label="#"
                  width="70">
                </el-table-column>
                <el-table-column
                  prop="name"
                  label="Никнэйм"
                  width="100">
                </el-table-column>
                <el-table-column
                  prop="updated_at"
                  label="Дата, Время"
                  width="180">
                </el-table-column>
                <el-table-column
                  prop="currency"
                  label="Валюта"
                  width="90">
                </el-table-column>
                <el-table-column
                  prop="amount"
                  label="Сумма, BTC">
                </el-table-column>
                <el-table-column
                  prop="bonuse"
                  label="Бонус (%)"
                  align="center"
                  width="110">
                </el-table-column>
                <el-table-column
                  prop="tokens"
                  label="Токены">
                </el-table-column>
                <el-table-column
                  label="Hash"
                  width="120">
                  <template scope="scope">
                    <a target="_blank" :href="'https://blockexplorer.com/tx/' + scope.row.hash">
                        <el-button
                          type="text"
                          size="small">
                          Link
                        </el-button>
                    </a>
                  </template>
                </el-table-column>
            </data-tables>
        </el-col>
    </el-row>
</template>

<script>
import api from '../../api'
import DataTables from 'vue-data-tables'
import lang from 'element-ui/lib/locale/lang/en'
import locale from 'element-ui/lib/locale'
locale.use(lang)

export default {
    props: ['tableData'],
    data () {
        return {
          // investors: null
        }
    },
    created() {
      // this.error = this.ico = null
      // let that = this
      // api.ico.investors(function(data) {
      //   // console.log(data)
      //   that.investors = data.data_provider.allModels
      // });
    },
    components: {
      DataTables
    }
}
</script>

<style>
.el-table {
    border: 0;
}
.el-table__header-wrapper thead div {
    color: #00a3e5;
    padding-top: 21px;
    padding-bottom: 26px;
    /*text-align: center;*/
    background-color: #fff
}
</style>