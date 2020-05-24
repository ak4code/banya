import Vue from 'vue'
import store from './store'
import UIkit from 'uikit'
import '@/assets/styles/styles.scss'

window.UIkit = UIkit

Vue.config.productionTip = false

new Vue({
  store,
  el: '#b-app'
})
