<template>
  <div class="b-product__card uk-border-rounded">
    <a :href="product.url">
      <div class="b-product__image">
        <img :src="product.medium_img" :alt="product.name">
      </div>
      <div class="b-product__info uk-padding-small">
        <div class="b-product__price uk-margin-small">
          {{ product.price }} <small>₽</small>
        </div>
        <div class="b-product__name uk-margin-small">
          {{ product.name }}
        </div>

      </div>
    </a>
    <a v-if="check(product.id)" class="uk-button uk-button-danger" href="/catalog/cart/">
      <span>Оформить</span>
    </a>
    <a class="uk-button uk-button-primary" v-else v-on:click.prevent="addItem(product)">
      <span>В корзину</span>
    </a>
  </div>
</template>

<script>
    import { mapActions, mapGetters } from 'vuex'

    export default {
        name: 'product',
        props: ['product'],
        computed: {
            ...mapGetters({
                check: 'cart/checkById'
            })
        },
        methods: {
            ...mapActions({
                addItem: 'cart/addItem'
            })
        }
    }
</script>

<style scoped>

</style>
