import queryString from 'query-string'

export const listing = {
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
  mounted () {
    this.getResults(queryString.parse(document.location.search))
  },
  methods: {
    getResults (params) {
      this.$axios.get(this.endpoint, {
        params: params
      })
        .then(res => {
          this.page = res.data
        })
        .catch(err => console.error(err))
    },
    scrollUp () {
      UIkit.scroll().scrollTo(document.getElementsByClassName('uk-breadcrumb'))
    },
    nextPage () {
      history.pushState(null, null, `?page=${this.page.next}`)
      this.getResults(queryString.parse(`?page=${this.page.next}`))
      this.scrollUp()
    },
    numPage (num) {
      history.pushState(null, null, `?page=${num}`)
      this.getResults(queryString.parse(`?page=${num}`))
      this.scrollUp()
    },
    previousPage () {
      history.pushState(null, null, `?page=${this.page.previous}`)
      this.getResults(queryString.parse(`?page=${this.page.previous}`))
      this.scrollUp()
    }
  }
}
