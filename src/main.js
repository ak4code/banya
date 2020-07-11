import Vue from 'vue'
import './plugins/axios'
import { Vue2Storage } from 'vue2-storage'
import store from './store'
import UIkit from 'uikit'
import Icons from 'uikit/dist/js/uikit-icons'
import '@/assets/styles/styles.scss'
import StoreMenu from '@/components/store/StoreMenu'
import ProductList from '@/components/store/ProductList'
import CartButton from '@/components/store/CartButton'

Vue.use(Vue2Storage, {
  prefix: 'app_',
  driver: 'local',
  ttl: 60 * 60 * 24 * 1000 // 24 часа
})

UIkit.use(Icons)
window.UIkit = UIkit

Vue.config.productionTip = false

new Vue({
  store,
  el: '#b-app',
  components: {
    StoreMenu,
    ProductList,
    CartButton
  }
})
