<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="left = !left" />
        &nbsp;
        &nbsp;
        &nbsp;
        <q-avatar>
          <img src="~assets/images/logo.png" style="width: 500%; margin-left: auto; margin-right: auto;">
        </q-avatar>
        <q-toolbar-title style="text-align: center;">
          TEMPONOMINA
        </q-toolbar-title>
        <q-space />
        <div class="q-gutter-sm row items-center no-wrap">
          <q-btn dense flat>
            <q-menu auto-close>
              <q-list dense>
              </q-list>
            </q-menu>
          </q-btn>
          <q-btn-dropdown round flat icon="person">
            <div class="row no-wrap q-pa-md">
              <div class="column items-center">
                <q-avatar @click="editing" class="cursor" size="72px">
                  <img alt="" src="https://cdn.quasar.dev/img/boy-avatar.png">
                </q-avatar>
                <div @click="editing" class="text-subtitle1 q-mt-md q-mb-xs cursor">{{full_name}}</div>
                <q-btn color="primary" label="Cerrar sesión" push size="sm" @click="logout" v-close-popup/>
              </div>
            </div>
          </q-btn-dropdown>
        </div>
      </q-toolbar>
    </q-header>
    <q-drawer :width="200" show-if-above v-model="left" side="left" bordered  content-class="bg-blue-grey-10 text-white">
      <q-list>
       <q-item clickable :to="{name: 'index'}" exact v-ripple exact-active-class="text-white bg-primary">
          <q-item-section avatar>
            <q-icon name="home" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Inicio</q-item-label>
          </q-item-section>
        </q-item>
        <Can I="read" an="Usuarios">
          <q-item clickable :to="{name: 'usuarios'}" exact v-ripple exact-active-class="text-white bg-primary">
            <q-item-section avatar>
              <q-icon name="person" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Usuarios</q-item-label>
            </q-item-section>
          </q-item>
        </Can>
      </q-list>
    </q-drawer>
    <q-dialog v-model="toolbar">
      <q-card style="width: 700px; max-width: 80vw;">
        <q-card-section class="row items-center">
          <div class="text-h6">Mi perfil</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>
        <q-banner class="bg-grey-3">
          <template v-slot:avatar>
            <q-icon name="warning" color="warning" />
          </template>
          Los campos marcados con (*) son obligatorios
        </q-banner>
        <q-card-section>
          <q-form ref="form">
            <div class="row justify-around">
              <div class="col-md-5">
                <q-input filled v-model="first_name" label="Nombres *" lazy-rules :rules="[ val => val && val.length > 0 || 'El campo es obligatorio']"/>
              </div>
              <div class="col-md-5">
                <q-input filled v-model="last_name" label="Apellidos *" lazy-rules :rules="[ val => val && val.length > 0 || 'El campo es obligatorio']"/>
              </div>
            </div>
            <div class="row justify-around">
              <div class="col-md-11">
                <q-input autocomplete="off" filled v-model="email" label="Correo electrónico *" lazy-rules :rules="[ val => val && val.length > 0 || 'El campo es obligatorio']"/>
              </div>
            </div>
            <div class="row justify-around">
              <div v-if="nuevo_password" class="col-md-5">
                <q-input autocomplete="off" type="password" filled v-model="actual_password" label="Contraseña *" lazy-rules :rules="[ val => val && val.length > 0 || 'El campo es obligatorio']"/>
              </div>
              <div v-else class="col-md-5">
                <q-input autocomplete="off" type="password" filled v-model="actual_password" label="Contraseña"/>
              </div>
              <div class="col-md-5">
                <q-input autocomplete="off" type="password" filled v-model="nuevo_password" label="Nueva contraseña *"/>
              </div>
            </div>
          </q-form>
        </q-card-section>
        <q-card-actions align="right" class="bg-white text-teal">
          <q-btn label="Actualizar" @click.prevent="onEdit" color="primary"/>
          <q-btn label="Cancelar" v-close-popup color="negative"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import axios from 'axios'
const path = 'seguridad/perfil/'
export default {
  data () {
    return {
      left: false,
      toolbar: false,
      first_name: null,
      last_name: null,
      email: null,
      actual_password: null,
      nuevo_password: null,
      full_name: null
    }
  },

  mounted () {
    this.loadUSer()
  },

  methods: {
    logout () {
      this.$store.dispatch('auth/logout').then(_success => {
        this.$router.push('/login')
      })
    },

    loadUSer () {
      axios.get(path).then(response => {
        this.first_name = response.data.first_name
        this.last_name = response.data.last_name
        this.email = response.data.email
        this.full_name = this.first_name + ' ' + this.last_name
      })
    },

    editing () {
      this.toolbar = true
      this.actual_password = null
      this.nuevo_password = null
    },

    onEdit () {
      this.$refs.form.validate().then(success => {
        if (success) {
          axios.put(path, {
            first_name: this.first_name,
            last_name: this.last_name,
            email: this.email,
            actual_password: this.actual_password,
            nuevo_password: this.nuevo_password
          }).then(_response => {
            this.toolbar = false
            this.loadUSer()
          })
        }
      })
    }
  }
}
</script>
<style lang="sass">
  .cursor
    cursor: pointer
</style>
