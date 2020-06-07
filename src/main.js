import Vue from 'vue'
import './plugins/axios'
import store from './store'
import UIkit from 'uikit'
import Icons from 'uikit/dist/js/uikit-icons'
import '@/assets/styles/styles.scss'
import StoreMenu from '@/components/store/StoreMenu'
import ProductList from '@/components/store/ProductList'
import CartButton from '@/components/store/CartButton'

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
