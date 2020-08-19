const cart = {
  namespaced: true,
  state: () => ({
    items: []
  }),
  mutations: {
    ADD_ITEM (state, item) {
      state.items.push({
        id: item.id,
        name: item.name,
        price: +item.price,
        quantity: 1,
        amount: +item.price,
        in_stock: item.in_stock,
        image: item.medium_img
      })
    },
    CHANGE_QUANTITY (state, payload) {
      state.items[payload.idx].quantity = payload.quantity
      state.items[payload.idx].amount = state.items[payload.idx].price * state.items[payload.idx].quantity
    },
    REMOVE_ITEM (state, payload) {
      state.items.splice(payload, 1)
    },
    SET_CART (state, items) {
      state.items = items
    }
  },
  actions: {
    async addItem ({ commit, dispatch }, id) {
      const { data } = await this._vm.$axios.get(`/api/store/products/${id}/`)
      commit('ADD_ITEM', data)
      dispatch('saveCart')
    },
    getCart ({ state, commit }) {
      if (!this._vm.$storage.get('cart')) {
        this._vm.$storage.set('cart', state.items)
      }
      commit('SET_CART', this._vm.$storage.get('cart'))
    },
    changeQuantity ({ commit, dispatch }, payload) {
      commit('CHANGE_QUANTITY', payload)
      dispatch('saveCart')
    },
    removeItem ({ commit, dispatch }, payload) {
      commit('REMOVE_ITEM', payload)
      dispatch('saveCart')
    },
    saveCart ({ state }) {
      this._vm.$storage.set('cart', state.items)
    }
  },
  getters: {
    itemById: state => id => {
      return state.items.findIndex(item => item.id === id)
    },
    checkById: state => id => {
      return state.items.find(i => i.id === +id)
    },
    totalAmount: state => {
      return state.items.reduce((a, b) => +a + +b.amount, 0)
    },
    getItems: state => {
      return state.items
    }
  }
}

export default cart
