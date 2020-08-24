<template>
  <div class="b-header__slider">
    <div class="uk-container">
      <div class="uk-position-center uk-text-center" v-if="!categories">
        <span class="b-header__slider__text">Добро пожаловать!</span>
      </div>
      <div class="uk-position-relative uk-light" tabindex="-1"
           uk-slideshow="min-height: 420; max-height: 440; animation: scale; autoplay: true; autoplay-interval: 2000; pause-on-hover: false"
           v-else>
        <ul class="uk-slideshow-items">
          <li v-for="c in categories" :key="c.id">
            <a :href="c.url">
              <div class="uk-position-center uk-text-center">
                <span class="b-header__slider__text">{{ c.name }}</span>
              </div>
            </a>
          </li>
        </ul>
        <a class="uk-position-center-left uk-position-small uk-hidden-hover" href="#" uk-slidenav-previous
           uk-slideshow-item="previous"></a>
        <a class="uk-position-center-right uk-position-small uk-hidden-hover" href="#" uk-slidenav-next
           uk-slideshow-item="next"></a>
      </div>
    </div>
  </div>
</template>

<script>
  import $ from 'jquery'
  import 'jquery.ripples'

  export default {
    name: 'header-slider',
    data: () => ({
      categories: null
    }),
    created() {
      this.getCategories()
    },
    mounted() {
      $('.b-header__slider').ripples(
              {
                dropRadius: 40,
                perturbance: 0.01
              })
    },
    methods: {
      async getCategories() {
        await this.$axios.get('/api/store/categories')
                .then(res => {
                  this.categories = res.data
                  this.loading = !this.loading
                })
                .catch(err => console.error(err))
      }
    }
  }
</script>

<style scoped>

</style>
