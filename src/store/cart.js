const cart = {
  namespaced: true,
  state: () => ({
    items: []
  }),
  mutations: {
    ADD_ITEM (state, item) {
      state.items.push({ id: item.id, name: item.name, price: +item.price, quantity: 1, amount: +item.price })
    },
    INCREMENT_QUANTITY (state, idx) {
      state.items[idx].quantity += 1
      state.items[idx].amount = state.items[idx].price * state.items[idx].quantity
    },
    SET_CART (state, items) {
      state.items = items
    }
  },
  actions: {
    addItem ({ state, getters, commit, dispatch }, item) {
      if (getters.itemById(item.id) !== -1) {
        commit('INCREMENT_QUANTITY', getters.itemById(item.id))
      } else {
        commit('ADD_ITEM', item)
      }
      dispatch('saveCart')
    },
    getCart ({ state, commit }) {
      if (!this._vm.$storage.get('cart')) {
        this._vm.$storage.set('cart', state.items)
      }
      commit('SET_CART', this._vm.$storage.get('cart'))
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
    }
  }
}

export default cart
