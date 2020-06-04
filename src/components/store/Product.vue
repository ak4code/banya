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
        <button class="uk-button uk-button-primary" v-on:click.prevent="addItem(product)">В корзину</button>
    </div>
</template>

<script>
    import { mapActions } from 'vuex'

    export default {
        name: "product",
        props: ['product'],
        methods: {
            ...mapActions({
                addItem: 'cart/addItem',
            })
        }
    }
</script>

<style scoped>

</style>