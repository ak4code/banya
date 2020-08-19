<template>
  <div class="store-menu uk-margin-bottom">
    <div class="uk-card uk-card-default uk-border-rounded uk-overflow-hidden uk-box-shadow-small">
      <ul class="uk-nav b-storemenu" v-if="!loading">
        <li v-for="category in categories" v-bind:class="currentCategory(category.id)" :key="category.id">
          <a :href="category.url" class="uk-flex uk-flex-between uk-flex-middle" :title="category.name">
            <div class="uk-width-expand">{{ category.name }}</div>
            <div class="b-counter uk-width-auto">{{ category.counts }}</div>
          </a>
        </li>
      </ul>
      <div v-else style="min-height: 250px;" class="uk-text-center">
        <span uk-spinner="ratio: 4.5"></span>
      </div>
    </div>
  </div>
</template>

<script>
    export default {
        name: 'store-menu',
        props: {
            id: Number
        },
        data: () => ({
            categories: [],
            loading: true
        }),
        created () {
            this.getCategories()
        },
        mounted () {
        },
        computed: {},
        methods: {
            async getCategories () {
                await this.$axios.get('/api/store/categories')
                    .then(res => {
                        this.categories = res.data
                        this.loading = !this.loading
                    })
                    .catch(err => console.error(err))
            },
            currentCategory: function (id) {
                if (this.id === id) return 'active'
            }
        }
    }
</script>

<style scoped>

</style>
