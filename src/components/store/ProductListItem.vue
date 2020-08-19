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
    <buy-button :id="product.id"></buy-button>
  </div>
</template>

<script>
    import BuyButton from './BuyButton'

    export default {
        name: 'product-list-item',
        props: ['product'],
        components: {
            BuyButton
        }
    }
</script>

<style scoped>

</style>
