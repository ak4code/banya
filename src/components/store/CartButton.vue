<template>
  <div class="cart-button">
    <span class="uk-margin-small-right" uk-icon="icon: cart"></span> <small>{{totalAmount}} руб.</small>
  </div>
</template>

<script>
    import { mapGetters } from 'vuex'

    export default {
        name: 'cart-button',
        data: () => ({}),
        computed: {
            ...mapGetters({
                totalAmount: 'cart/totalAmount'
            })
        }
    }
</script>

<style scoped>

</style>
