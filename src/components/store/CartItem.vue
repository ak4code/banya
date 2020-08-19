<template>
  <div class="cart-item uk-flex uk-flex-wrap uk-flex-middle uk-grid-small">
    <div class="item-image uk-width-auto">
      <img :src="item.image" :alt="item.name" width="100" height="100">
    </div>
    <div class="item-info uk-width-expand">
      <div class="uk-flex uk-flex-wrap uk-flex-middle uk-grid-small">
        <div class="uk-width-expand">
          <h5 class="uk-margin-small-bottom">{{item.name}}</h5>
          <div class="uk-label uk-label-success uk-margin-bottom" v-if="item.in_stock">В наличии</div>
          <div class="uk-label uk-label-warning uk-margin-bottom" v-else>Под заказ</div>
        </div>
        <div class="uk-width-1-5@m uk-text-center">
          <input class="uk-input" min="1" max="999" type="number" :value="item.quantity" @change="updateQuantity">
          <small>{{item.price}} / шт.</small>
        </div>
        <div class="uk-width-1-5@m uk-flex-first uk-flex-last@m">
          <div class="uk-text-large uk-text-bold">
            {{item.amount}} ₽
          </div>
        </div>
      </div>
    </div>
    <div class="uk-width-auto uk-padding-small">
      <a @click="removeItem(idx)" uk-icon="trash"></a>
    </div>
  </div>
</template>

<script>
    import { mapActions } from 'vuex'

    export default {
        name: 'cart-item',
        props: ['item', 'idx'],
        methods: {
            ...mapActions({
                changeQuantity: 'cart/changeQuantity',
                removeItem: 'cart/removeItem'
            }),
            updateQuantity (e) {
                this.changeQuantity({ idx: this.idx, quantity: +e.target.value })
            }
        }
    }
</script>

<style scoped>
  .cart-item {
    padding-top: 10px;
    padding-bottom: 10px;
    border-bottom: 1px solid #ddd;
    width: 100%;
    margin: 0;
  }

  .cart-item:first-child {
    border-top: 1px solid #ddd;
  }
</style>
