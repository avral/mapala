<template>
    <div class="tagCloud">
        <a v-if="lang == 'ru'" v-for="tag in tags" @click="setTags(tag.value)" href="javascript:void(0)">
            <span class="tag" v-bind:style="tag.style">{{tag.name}}</span>
        </a>
    </div>
</template>

<script>
    import {detransliterate} from '../utils'
    import Vue from 'vue';

    export default {
        data() {
            return {
              lang: Vue.config.lang,
                tags: [
                    {
                        name: 'Открытый код',
                        value: 'ru--otkrytyij-kod',
                        style: {
                            fontFamily: 'PTSans-Narrow',
                            fontSize: '24px',
                         },
                     },
                    {
                        name: 'Блог',
                        value: 'ru--blog',
                        style: {
                            fontFamily: 'TSans-Narrow',
                            fontSize: '30px',
                            fontWeight: 'bold'
                        }
                    },
                    {
                        name: 'ICO',
                        value: 'ico',
                        style: {
                            fontFamily: 'PTSans-Narrow',
                            fontSize: '36px',
                            fontWeight: 'bold'
                        }
                    },
                    {
                        name: 'Сайт',
                        value: 'ru--saijt',
                        style: {
                            fontFamily: 'PTSans-Narrow',
                            fontSize: '24px',
                        },
                    },
                    {
                        name: 'Команда',
                        value: 'ru--komanda',
                        style: {
                            fontFamily: 'HelveticaNeueCyr',
                             fontSize: '36px',
                             fontWeight: 500,
                         }
                    },
                    {
                        name: 'Сообщество',
                        value: 'ru--soobshchestvo',
                        style: {
                            fontFamily: 'TimesNewRomanPSMT',
                             fontSize: '30px',
                         }

                    },
                    {
                        name: 'Разное',
                        value: 'ru--raznoe',
                        style: {
                            fontFamily: 'PTSans-Narrow;',
                            fontSize: '16px',
                            fontWeight: 'bold'
                        }
                    }
                ]
            }
        },
        methods: {
            setTags(tag) {
                this.$store.dispatch('setTags', tag)
            }
        }
    }
</script>
<style scoped>
    .tagCloud {
        text-align: center;
        position: relative;
        top: 180px;
        max-width: 300px;
        text-align: center;
        left: 30%;
    }
    .tag {
        display: inline-block;
        padding: 3px 10px;
        color: #fab3c6;
    }
</style>
