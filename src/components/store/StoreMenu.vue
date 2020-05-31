<template>
  <div class="store-menu uk-margin-top">
    <div class="uk-card uk-card-default uk-border-rounded uk-overflow-hidden uk-box-shadow-small">
      <ul class="uk-nav b-storemenu">
        <li v-for="category in categories" v-bind:class="{ 'active': id == category.id }" :key="category.id">
          <a :href="category.url" class="uk-flex uk-flex-between uk-flex-middle">
            <div class="uk-width-expand">{{category.name}}</div>
            <div class="b-counter uk-width-auto">{{category.counts}}</div>
          </a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
    export default {
        name: 'store-menu',
        props: ['id'],
        data: () => ({
            categories: []
        }),
        created () {
            this.getCategories()
        },
        computed: {
            currentCategory: function (id) {
                return {
                    active: this.id && id
                }
            }
        },
        methods: {
            getCategories () {
                this.$axios.get('/api/store/categories')
                    .then(res => {
                        this.categories = res.data
                    })
                    .catch(err => console.error(err))
            }
        }
    }
</script>

<style scoped>

</style>
