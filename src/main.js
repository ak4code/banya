import Vue from 'vue'
import './plugins/axios'
import { Vue2Storage } from 'vue2-storage'
import store from './store'
import UIkit from 'uikit'
import Icons from 'uikit/dist/js/uikit-icons'
import '@/assets/styles/styles.scss'
import ProductList from '@/components/store/ProductList'
import CartButton from '@/components/store/CartButton'
import BuyButton from '@/components/store/BuyButton'
import Cart from '@/components/store/Cart'
import HeaderSlider from '@/components/core/HeaderSlider'

Vue.use(Vue2Storage, {
  prefix: 'app_',
  driver: 'local',
  ttl: 60 * 60 * 24 * 1000 // 24 часа
})

UIkit.use(Icons)
window.UIkit = UIkit

Vue.config.productionTip = false

const app = new Vue({
  store,
  el: '#b-app',
  components: {
    BuyButton,
    ProductList,
    CartButton,
    Cart,
    HeaderSlider
  }
})

store.$app = app
