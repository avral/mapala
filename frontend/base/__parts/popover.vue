<template>
  <div class="poster__Button">
    <el-popover
      ref="popover4"
      placement="bottom"
      width="400"
      trigger="click">

      <div class="poster__Column">
        <h4 style="">Город</h4>
        <!--<div class="el-transfer-panel__filter el-input el-input&#45;&#45;small"><i class="el-input__icon el-icon-search"></i><input autocomplete="off" placeholder="Поиск" size="small" icon="search" type="text" rows="2" validateevent="true" class="el-input__inner"></div>-->

        <ul style="margin: 0;padding: 0;">
          <li style="list-style: none;font-size: 12px;color: #6984a8;">
            <router-link :to="{ path: '/rnd' }" class="poster_city_link">Ростов-на-Дону</router-link>
          </li>
        </ul>
      </div>

      <div class="poster__Column">
        <h4 style="">Афиша</h4>

        <ul style="margin: 0;padding: 0;">
          <li style="list-style: none;font-size: 12px;color: #6984a8;">
            <a class="poster_city_link"></a>
          </li>
        </ul>
      </div>

      <div class="poster__Column">
        <h4 style="">Чат</h4>
      </div>

      <div class="poster__Column">
        <h4 style="">Группа Мапала</h4>
      </div>
    </el-popover>





    <el-button v-popover:popover4>
      {{ $t('poster') }}
      <span class="caret"></span>
    </el-button>
  </div>
</template>

<script>
import { mapState, mapActions, mapMutations } from 'vuex'

export default {
  mounted () {

  },

  data () {
    return {
      gridData: [{
        date: '2016-05-02',
        name: 'Jack',
        address: 'New York City'
      }, {
        date: '2016-05-04',
        name: 'Jack',
        address: 'New York City'
      }, {
        date: '2016-05-01',
        name: 'Jack',
        address: 'New York City'
      }, {
        date: '2016-05-03',
        name: 'Jack',
        address: 'New York City'
      }]
    }
  },

  methods: {}
}
</script>

<style scoped>
  .caret {
    display: inline-block;
    width: 0;
    height: 0;
    vertical-align: middle;
    border-top: 4px dashed;
    border-right: 4px solid transparent;
    border-left: 4px solid transparent;
    margin-left: 6px;
  }
  .poster__Button {
    margin-left: 10px;
  }

  .poster__Button .el-button {
    background: transparent !important;
    border: none !important;
    font-size: 12px !important;
    color: #8DAFE1 !important;
  }
</style scoped>
