import Vue from 'vue'
import './plugins/axios'
import store from './store'
import UIkit from 'uikit'
import '@/assets/styles/styles.scss'
import StoreMenu from '@/components/store/StoreMenu'

window.UIkit = UIkit

Vue.config.productionTip = false

new Vue({
  store,
  el: '#b-app',
  components: {
    StoreMenu
  }
})
