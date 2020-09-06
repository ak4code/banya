<template>
  <div class="cart uk-flex uk-flex-wrap uk-grid-small">
    <div class="uk-width-2-3@m" v-if="!checkout">
      <div class="uk-card uk-padding-remove uk-card-default uk-margin-small-bottom" v-if="items.length">
        <cart-item v-for="(item, index) in items" :key="item.id" :item="item" :idx="index"></cart-item>
        <div class="uk-padding uk-text-right">
          <h4 class="uk-margin-remove uk-text-bold">Итого: {{totalAmount}} ₽ *</h4>
          <small class="uk-text-muted">* Без учета стоимости доставки</small>
        </div>
      </div>
      <div class="uk-card uk-padding-remove uk-card-default uk-margin-small-bottom" v-else>
        <div class="uk-text-center uk-text-large uk-padding-large">
          <p>В вашей корзине еще нет товаров.</p>
        </div>
      </div>
    </div>
    <div class="uk-width-1-3@m" v-if="!checkout">
      <div class="uk-card uk-card-small uk-card-body uk-card-default">
        <form @submit.prevent="checkoutForm" method="post">
          <slot name="csrf"></slot>
          <fieldset class="uk-fieldset">
            <legend class="uk-legend">Оформление заказа</legend>
            <div class="uk-margin">
              <label class="uk-form-label" for="customer_name">ФИО</label>
              <input class="uk-input" name="customer_name" id="customer_name" type="text"
                     placeholder="ФИО (пр. Иванов Иван Иванович)"
                     required v-model="customer.first_name">
            </div>
            <div class="uk-margin">
              <label class="uk-form-label" for="customer_phone">Телефон</label>
              <input class="uk-input" name="customer_phone" id="customer_phone" minlength="5" maxlength="15" type="text"
                     placeholder="Телефон"
                     required
                     v-model="customer.username">
            </div>
            <div class="uk-margin">
              <label class="uk-form-label" for="customer_email">Email</label>
              <input class="uk-input" name="customer_email" id="customer_email" type="email" placeholder="E-mail"
                     v-model="customer.email"
                     required>
            </div>
            <div class="uk-margin" v-if="customer.id">
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
          <button class="uk-button uk-button-secondary uk-width-1-1 uk-margin-small-bottom" :disabled="!items.length">
            <span v-if="!customer.id">Продолжить</span>
            <span v-else>Оформить</span>
          </button>
        </form>
      </div>
    </div>
    <div class="uk-width-1-1" v-if="checkout">
      <div class="uk-card uk-card-small uk-card-body uk-card-default">
        <h1 class="uk-text-center uk-h2 uk-text-bold">Вы успешно оформили заказ!</h1>
        <div class="uk-flex uk-flex-middle uk-flex-center">
          <div class="uk-text-center">
            <div class="uk-padding-small uk-animation-toggle" tabindex="0">
              <span class="uk-animation-shake" uk-icon="icon: check; ratio: 5"
                    style="color: green;border-radius: 50%;border: 4px solid;padding: 10px;"></span>
            </div>
            <div class="uk-padding-small">
              <div class="uk-text-lead">{{checkout.customer_info.first_name}} в ближайшее время ваш заказ обработает
                менеджер магазина.
              </div>
            </div>
            <a href="/" class="uk-button uk-text-large uk-button-text uk-margin">Вернуться на главную</a>
          </div>
        </div>
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
                first_name: null,
                username: null,
                email: null
            },
            shipping: {
                type: 'pickup',
                city: null,
                address: null
            },
            checkout: null
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
                if (!this.customer.id) {
                    await this.$axios.post('/api/store/cart/', this.customer)
                        .then(res => {
                            this.customer = res.data
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
                        .then(res => {
                            this.checkout = res.data
                            this.$store.dispatch('cart/clearCart')
                        })
                        .catch(err => console.log({ err }))
                }
            }
        }
    }
</script>

<style scoped>

</style>
