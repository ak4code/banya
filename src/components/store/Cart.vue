<template>
  <div class="cart uk-flex uk-flex-wrap uk-grid-small">
    <div class="uk-width-2-3@m">
      <div class="uk-card uk-padding-remove uk-card-default uk-margin-small-bottom">
        <cart-item v-for="(item, index) in items" :key="item.id" :item="item" :idx="index"></cart-item>
        <div class="uk-padding uk-text-right">
          <h4 class="uk-margin-remove uk-text-bold">Итого: {{totalAmount}} ₽ *</h4>
          <small class="uk-text-muted">* Без учета стоимости доставки</small>
        </div>
      </div>
    </div>
    <div class="uk-width-1-3@m">
      <div class="uk-card uk-card-small uk-card-body uk-card-default">
        <form @submit.prevent="checkoutForm" method="post">
          <slot name="csrf"></slot>
          <fieldset class="uk-fieldset">
            <legend class="uk-legend">Оформление заказа</legend>
            <div class="uk-margin" v-if="!customer.isAuth">
              <label class="uk-form-label" for="customer_name">ФИО</label>
              <input class="uk-input" name="customer_name" id="customer_name" type="text"
                     placeholder="ФИО (пр. Иванов Иван Иванович)"
                     required v-model="customer.name">
            </div>
            <div class="uk-margin" v-if="!customer.isAuth">
              <label class="uk-form-label" for="customer_phone">Телефон</label>
              <input class="uk-input" name="customer_phone" id="customer_phone" minlength="5" maxlength="15" type="text"
                     placeholder="Телефон"
                     required
                     v-model="customer.phone">
            </div>
            <div class="uk-margin" v-if="!customer.isAuth">
              <label class="uk-form-label" for="customer_email">Email</label>
              <input class="uk-input" name="customer_email" id="customer_email" type="email" placeholder="E-mail"
                     v-model="customer.email"
                     required>
            </div>
            <div class="uk-margin" v-if="customer.isAuth">
              <div class="uk-form-label">Способ доставки</div>
              <div class="uk-form-controls">
                <label><input class="uk-radio" value="pickup" type="radio" name="shipping" v-model="shipping.type">
                  Самовывоз</label><br>
                <label><input class="uk-radio" value="shipping" type="radio" name="shipping" v-model="shipping.type">
                  Доставка</label>
              </div>
              <div class="uk-margin" v-if="shipping.type === 'shipping'">
                <div class="uk-margin">
                  <input class="uk-input" name="shipping_city" v-model="shipping.city" type="text" placeholder="Город">
                </div>
                <div class="uk-margin">
                  <input class="uk-input" name="shipping_address" v-model="shipping.address" type="text"
                         placeholder="Адрес">
                </div>
              </div>
            </div>
          </fieldset>
          <button class="uk-button uk-button-secondary uk-width-1-1 uk-margin-small-bottom">
            <span v-if="!customer.isAuth">Продолжить</span>
            <span v-else>Оформить</span>
          </button>
        </form>

      </div>
    </div>
  </div>
</template>

<script>
    import { mapGetters } from 'vuex'
    import CartItem from './CartItem'

    export default {
        name: 'cart',
        data: () => ({
            customer: {
                id: null,
                name: null,
                phone: null,
                email: null,
                isAuth: false
            },
            shipping: {
                type: 'pickup',
                city: null,
                address: null
            }
        }),
        components: { CartItem },
        computed: {
            ...mapGetters({
                items: 'cart/getItems',
                totalAmount: 'cart/totalAmount'
            })
        },
        methods: {
            checkoutForm: async function (e) {
                if (!this.customer.isAuth) {
                    await this.$axios.post('/api/store/cart/', this.customer)
                        .then(res => {
                            console.log({ res });
                            this.customer.isAuth = true
                            this.customer.id = res.data.user_id
                        })
                        .catch(err => console.log({ err }))
                } else {
                    await this.$axios.post('/api/store/orders/', {
                        shipping_type: this.shipping_type,
                        shipping_city: this.shipping.city,
                        shipping_address: this.shipping.address,
                        items: this.items,
                        customer: this.customer.id
                    })
                        .then(res => console.log({ res }))
                        .catch(err => console.log({ err }))
                }
            }
        }
    }
</script>

<style scoped>

</style>
