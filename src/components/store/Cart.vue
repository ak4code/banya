<template>
  <div class="cart uk-flex uk-flex-wrap uk-grid-small">
    <div class="uk-width-2-3@m">
      <div class="uk-card uk-padding-remove uk-card-default uk-margin-small-bottom">
        <cart-item v-for="(item, index) in items" :key="item.id" :item="item" :idx="index"></cart-item>
      </div>
    </div>
    <div class="uk-width-1-3@m">
      <div class="uk-card uk-card-small uk-card-body uk-card-default">
        <h4>Оформление</h4>
      </div>
    </div>
  </div>
</template>

<script>
    import { mapGetters } from 'vuex'
    import CartItem from './CartItem'

    export default {
        name: 'cart',
        components: { CartItem },
        computed: {
            ...mapGetters({
                items: 'cart/getItems'
            })
        }
    }
</script>

<style scoped>

</style>
