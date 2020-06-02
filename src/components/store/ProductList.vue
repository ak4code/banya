<template>
    <div class="b-product__list">
        <div class="uk-flex uk-flex-wrap uk-grid-small uk-child-width-1-2@s uk-child-width-1-3@m uk-child-width-1-4@l">
            <div class="uk-margin-bottom" v-for="product in page.results" :key="product.id">
                <product :product="product"></product>
            </div>
        </div>
        <div class="b-pagination" v-if="page.num_pages > 1">
            <div class="uk-card uk-card-small uk-card-body uk-card-default uk-margin uk-border-rounded uk-box-shadow-medium">
                <ul class="uk-pagination uk-flex-center" uk-margin>
                    <li v-if="page.previous"><a v-on:click.prevent="previousPage"><span uk-pagination-previous></span></a></li>
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
    import queryString from 'query-string'
    import Product from "./Product";

    export default {
        name: "product-list",
        data: () => ({
            page: {
                count: null,
                next: null,
                previous: null,
                page_size: null,
                page_number: null,
                num_pages: null,
                results: []
            }
        }),
        components: {
            Product
        },
        created() {
            this.getProducts(queryString.parse(document.location.search))
        },
        methods: {
            getProducts(params) {
                this.$axios.get('/api/store/products', {
                    params: params
                })
                    .then(res => {
                        this.page = res.data
                    })
                    .catch(err => console.error(err))
            },
            nextPage() {
                history.pushState(null, null, `?page=${this.page.next}`)
                this.getProducts(queryString.parse(`?page=${this.page.next}`))
                UIkit.scroll().scrollTo(document.getElementsByClassName('b-page__title'))
            },
            numPage(num) {
                history.pushState(null, null, `?page=${num}`)
                this.getProducts(queryString.parse(`?page=${num}`))
                UIkit.scroll().scrollTo(document.getElementsByClassName('b-page__title'))
            },
            previousPage() {
                history.pushState(null, null, `?page=${this.page.previous}`)
                this.getProducts(queryString.parse(`?page=${this.page.previous}`))
                UIkit.scroll().scrollTo(document.getElementsByClassName('b-page__title'))
            }
        }
    }
</script>

<style scoped>

</style>