<template>
  <div class="bg-grey window-height window-width row justify-center items-center">
    <div class="column">
      <div class="row">
        <h5 style="text-align: center;" class="text-h5 text-white q-my-md"> &nbsp; &nbsp; &nbsp; &nbsp;</h5>
      </div>
      <div class="row">
        <q-card square bordered class="q-pa-lg shadow-1">
          <img alt="" src="~assets/images/logo.png" style="width: 50%; display: block; margin-left: auto; margin-right: auto;">
          <q-form @submit="login" ref="formLogin">
            <q-card-section>
              <q-form class="q-gutter-md">
                <q-input square filled clearable v-model="username" label="Usuario" />
                <q-input square filled clearable v-model="password" type="password" label="Contraseña" />
              </q-form>
            </q-card-section>
            <q-card-actions class="q-px-md">
              <q-btn type="submit" unelevated color="primary" size="lg" class="full-width" label="Iniciar sesión" />
            </q-card-actions>
          </q-form>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script>
import { AbilityBuilder } from '@casl/ability'
import { mapState } from 'vuex'
export default {
  name: 'Login',
  data () {
    return {
      username: null,
      password: null
    }
  },

  methods: {
    login () {
      this.$store.dispatch('auth/login', {
        username: this.username,
        password: this.password
      }).then(_success => {
        this.$router.push({ name: 'usuarios' })
      })
    }

  },

  computed: {
    ...mapState({
      rol: state => state.auth.rol
    })
  },

  watch: {
    rol: function (val) {
      const { can, rules } = new AbilityBuilder()
      switch (val) {
        case 'AD':
          can('manage', 'all')
          break
        case 'CI':
          // se agregaran los permisos de ciudadanos
          break
        case 'CO':
          // se agregaran los permisos de consultas
          break
      }
      this.$ability.update(rules)
    }
  }
}
</script>

<style lang="stylus">
  .q-card
    width: 360px
</style>
