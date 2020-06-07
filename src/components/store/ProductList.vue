<template>
    <div class="b-product__list">
        <div class="uk-flex uk-flex-wrap uk-grid-small uk-child-width-1-2 uk-child-width-1-3@m uk-child-width-1-4@l">
            <div class="uk-margin-bottom" v-for="product in page.results" :key="product.id">
                <product :product="product"></product>
            </div>
        </div>
        <div class="b-pagination" v-if="page.num_pages > 1">
            <div class="uk-card uk-card-small uk-card-body uk-card-default uk-margin uk-border-rounded uk-box-shadow-medium">
                <ul class="uk-pagination uk-flex-center" uk-margin>
                    <li v-if="page.previous"><a v-on:click.prevent="previousPage"><span
                            uk-pagination-previous></span></a></li>
                    <li :class="[page.page_number == num ? 'uk-active' : '']" v-for="num in page.num_pages" :key="num">
                        <a v-on:click.prevent="numPage(num)"><span>{{num}}</span></a>
                    </li>
                    <li v-if="page.next"><a v-on:click.prevent="nextPage"><span uk-pagination-next></span></a></li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
    import Product from "./Product"
    import {listing} from "../mixins/listing"

    export default {
        name: "product-list",
        props: ['category'],
        mixins: [listing],
        data: () => ({
            endpoint: '/api/store/products'
        }),
        created() {
            if (this.category) this.endpoint += `?category=${this.category}`
        },
        components: {
            Product
        }
    }
</script>

<style scoped>

</style>
