<template>
  <div class="buy-button">
    <a v-if="check(id)" class="uk-button uk-button-danger" href="/catalog/cart/">
      <span>Оформить</span>
    </a>
    <a class="uk-button uk-button-primary" v-else v-on:click.prevent="addItem(id)">
      <span>В корзину</span>
    </a>
  </div>
</template>

<script>
    import { mapActions, mapGetters } from 'vuex'

    export default {
        name: 'buy-button',
        props: ['id'],
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
  .buy-button {
    width: 100%;
    display: flex;
    position: relative;
    flex-direction: column;
    flex: 1;
  }
</style>
