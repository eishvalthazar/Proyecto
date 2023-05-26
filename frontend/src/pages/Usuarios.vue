<template>
  <q-page class="q-pa-md q-gutter-sm">
    <div>
      <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
        <div>
          <q-space />
          <q-table dense :rows-per-page-options="[10, 15, 20, 25, 50, 0]" :pagination.sync="pagination" title="Usuarios" :data="data" :filter="filter" :columns="columns" row-key="name" >
            <template v-if="$can('create', 'Usuarios')" v-slot:top-left>
              <q-btn unelevated rounded icon="add" color="primary" @click="creating" label="Agregar"/>
              <q-space />
            </template>
            <template v-slot:top-right>
              <q-input dense debounce="300" v-model="filter" placeholder="Buscar">
                <template v-slot:append>
                  <q-icon name="search" />
                </template>
              </q-input>
            </template>
            <template v-slot:body="props">
              <q-tr :props="props">
                <q-td key="username" :props="props">
                  {{ props.row.username }}
                </q-td>
                <q-td key="first_name" :props="props">
                  {{ props.row.first_name }}
                </q-td>
                <q-td key="last_name" :props="props">
                  {{ props.row.last_name }}
                </q-td>
                <q-td key="email" :props="props">
                  {{ props.row.email }}
                </q-td>
                <q-td v-if="props.row.rol" key="rol" :props="props">
                  {{ props.row.rol.descripcion }}
                </q-td>
                <q-td v-else key="rol" :props="props">
                </q-td>
                <can I="update" an="Usuarios">
                  <q-td key="edit" :props="props">
                    <q-btn round size="xs" color="primary" icon="border_color" v-on:click="editing(props.row)" />
                  </q-td>
                </can>
                <can I="delete" an="Usuarios">
                  <q-td key="delete" :props="props">
                    <q-btn round size="xs" color="negative" icon="delete_forever" v-on:click="onDelete(props.row)" />
                  </q-td>
                </can>
              </q-tr>
            </template>
          </q-table>
        </div>
      </transition>
      <q-inner-loading :showing="visible">
        <q-spinner-pie color="primary" size="70px"/>
      </q-inner-loading>
    </div>
    <q-dialog v-model="toolbar" persistent>
      <q-card style="width: 700px; max-width: 80vw;">
        <q-card-section class="row items-center">
          <div class="text-h6">Usuario</div>
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
          <q-form ref="form" @submit.prevent="">
            <div class="row justify-around">
              <div class="col-md-5">
                <q-input filled v-model="username" label="Usuario *" lazy-rules :rules="[ val => val && val.length > 0 || 'El campo es obligatorio']"/>
              </div>
              <div class="col-md-5">
                <q-input filled v-model="first_name" label="Nombres *" lazy-rules :rules="[ val => val && val.length > 0 || 'El campo es obligatorio']"/>
              </div>
            </div>
            <div class="row justify-around">
              <div class="col-md-5">
                <q-input filled v-model="last_name" label="Apellidos *" lazy-rules :rules="[ val => val && val.length > 0 || 'El campo es obligatorio']"/>
              </div>
              <div class="col-md-5">
                <q-input filled v-model="email" label="Correo electrónico *" lazy-rules :rules="[ val => val && val.length > 0 || 'El campo es obligatorio']"/>
              </div>
            </div>
            <div class="row justify-around">
              <div class="col-md-11">
                <q-select use-input input-debounce="0" @filter="filterFnRoles" filled v-model="rol" :options="filterOptionsRoles" option-label="descripcion" option-value="codigo" label="Rol *"  emit-value map-options lazy-rules :rules="[ val => !!val || 'El campo es obligatorio']"/>
              </div>
            </div>
          </q-form>
        </q-card-section>
        <div class="row justify-between">
          <q-card-actions align="left" class="bg-white text-teal">
            <q-btn v-if="isEditing" label="Enviar contraseña" @click.prevent="onSendPassword" color="info"/>
          </q-card-actions>
          <q-card-actions align="right" class="bg-white text-teal">
            <q-btn v-if="!isEditing" label="Guardar" @click.prevent="onSubmit" color="primary"/>
            <q-btn v-else label="Actualizar" @click.prevent="onEdit" color="primary"/>
            <q-btn label="Cancelar" v-close-popup color="negative"/>
          </q-card-actions>
        </div>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<style lang="sass">
</style>

<script>
import axios from 'axios'
const path = 'seguridad/usuarios/'
export default {
  name: 'Usuarios',
  components: {
  },
  data () {
    return {
      toolbar: false,
      uuid: null,
      username: null,
      first_name: null,
      last_name: null,
      email: null,
      optionsRoles: [],
      filterOptionsRoles: [],
      rol: null,
      columns: [
        { name: 'username', align: 'center', label: 'Usuario', field: 'username', sortable: true },
        { name: 'first_name', align: 'center', label: 'Nombres', field: 'first_name', sortable: true },
        { name: 'last_name', align: 'center', label: 'Apellidos', field: 'last_name', sortable: true },
        { name: 'email', align: 'center', label: 'Correo electrónico', field: 'email', sortable: true },
        { name: 'rol', align: 'center', label: 'Rol', field: 'rol', sortable: true }
      ],
      data: [],
      filter: null,
      isEditing: false,
      visible: false,
      confirm: false,
      pagination: {
        page: 1,
        rowsPerPage: 10
      }
    }
  },

  mounted () {
    this.loadTable()
    this.loadSelectRoles()
    this.setColumns()
  },

  methods: {
    loadSelectRoles () {
      axios.get('seguridad/usuarios/roles/').then(response => {
        this.optionsRoles = response.data
        this.filterOptionsRoles = response.data
      })
    },

    setColumns () {
      if (this.$can('update', 'Usuarios')) {
        this.columns.push({ name: 'edit', align: 'center', label: 'Editar', field: 'edit', sortable: true })
      }

      if (this.$can('delete', 'Usuarios')) {
        this.columns.push({ name: 'delete', align: 'center', label: 'Eliminar', field: 'delete', sortable: true })
      }
    },

    filterFnRoles (val, update) {
      if (val === '') {
        update(() => {
          this.filterOptionsRoles = this.optionsRoles
        })
        return
      }

      update(() => {
        const needle = val.toLowerCase()
        this.filterOptionsRoles = this.optionsRoles.filter(v => v.descripcion.toLowerCase().indexOf(needle) > -1)
      })
    },
    onSubmit () {
      this.$refs.form.validate().then(success => {
        if (success) {
          axios.post(path, {
            username: this.username,
            first_name: this.first_name,
            last_name: this.last_name,
            email: this.email,
            rol: this.rol
          }).then(_response => {
            this.toolbar = false
            this.loadTable()
          })
        }
      })
    },

    loadTable () {
      this.visible = true
      axios.get(path).then(response => {
        this.data = response.data
        this.visible = false
      })
    },

    onEdit () {
      this.$refs.form.validate().then(success => {
        if (success) {
          axios.put(path + this.uuid + '/', {
            username: this.username,
            first_name: this.first_name,
            last_name: this.last_name,
            email: this.email,
            rol: this.rol
          }).then(_response => {
            this.toolbar = false
            this.loadTable()
          })
        }
      })
    },

    onDelete (row) {
      this.$q.dialog({
        title: 'Confirmación',
        message: 'Desea eliminar el registro?',
        ok: {
          label: 'Si',
          color: 'positive'
        },
        cancel: {
          label: 'No',
          color: 'negative'
        }
      }).onOk(() => {
        axios.delete(path + row.uuid + '/').then(_response => {
          this.loadTable()
        })
      })
    },

    onReset () {
      this.username = null
      this.first_name = null
      this.last_name = null
      this.email = null
      this.rol = null
    },

    creating () {
      this.onReset()
      this.isEditing = false
      this.toolbar = true
    },

    editing (row) {
      this.onReset()
      this.isEditing = true
      this.uuid = row.uuid
      this.username = row.username
      this.first_name = row.first_name
      this.last_name = row.last_name
      this.email = row.email
      if (row.rol) {
        this.rol = row.rol.codigo
      }
      this.toolbar = true
    },

    onSendPassword () {
      axios.get('seguridad/usuarios/generar_clave/' + this.uuid + '/').then(_response => {
        this.toolbar = false
      })
    }
  }
}
</script>
