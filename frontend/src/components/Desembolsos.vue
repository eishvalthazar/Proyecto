<template>
    <q-card style="width: 600px; max-width: 80vw;">
      <q-card-section class="row items-center">
        <div class="text-h5">Desembolso</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>
      <q-banner class="bg-grey-3">
        <template v-slot:avatar>
          <q-icon name="payments" color="green" />
        </template>
        Los campos marcados con (*) son obligatorios
      </q-banner>
      <q-card-section>
        <q-form ref="form">
          <div class="row q-col-gutter-sm">
            <div class="col-md-6">
              <q-input filled mask="###################" v-model="numero_credito" label="Número del crédito *" lazy-rules :rules="[val => val !== null && val !== '' || 'Este campo es obligatorio',]"/>
            </div>
          </div>
          <div>
            <div class="col-md-6">
              <q-input filled type="number" v-model="valor_desembolso" label="Valor total del crédito *" lazy-rules :rules="[val => val !== null && val !== '' || 'Este campo es obligatorio',]"/>
              <q-tooltip>No se permiten desembolsos iguales a 0</q-tooltip>
            </div>
            <div class="col-md-6">
              <q-input filled v-model="fecha_desembolso" mask="date" label="Fecha de desembolso *" lazy-rules :rules="[ val => val && val.length > 0 || 'El campo es obligatorio']">
                <template v-slot:append>
                  <q-icon name="event" class="cursor-pointer">
                    <q-popup-proxy ref="qDateProxy" cover transition-show="scale" transition-hide="scale">
                      <q-date v-model="fecha_desembolso" mask="YYYY-MM-DD">
                        <div class="row items-center justify-end">
                          <q-btn v-close-popup label="Cerrar" color="primary" flat />
                        </div>
                      </q-date>
                    </q-popup-proxy>
                  </q-icon>
                </template>
              </q-input>
            </div>
          </div>
        </q-form>
      </q-card-section>
      <q-card-actions align="right" class="bg-white text-teal">
        <q-btn v-if="!isEditing" :disable="disable" label="Guardar" @click.prevent="onSubmit" color="primary"/>
        <q-btn v-else label="Actualizar" @click.prevent="onEdit" color="primary"/>
        <q-btn label="Cancelar" v-close-popup color="negative"/>
      </q-card-actions>
    </q-card>
</template>

<script>
import axios from 'axios'
import moment from 'moment'
const path = 'creditos/desembolsos/'
export default {
  name: 'desembolsos',
  props: {
    desembolsos: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      numero_credito: null,
      valor_desembolso: 0,
      credito: null,
      fecha_desembolso: null,
      detalle_credito: this.desembolsos,
      isEditing: null,
      disable: true
    }
  },

  methods: {
    onReset () {
      this.numero_credito = null
      this.valor_desembolso = null
      this.fecha_desembolso = null
    },

    creating () {
      this.onReset()
      this.isEditing = false
    },

    editing (row) {
      this.onReset()
      this.isEditing = true
      this.uuid = row.uuid
      this.numero_credito = row.numero_credito
      this.valor_desembolso = row.valor_desembolso
      this.toolbar = true
    },

    onSubmit () {
      this.$refs.form.validate().then(success => {
        if (success) {
          axios.post('creditos/desembolsos/', {
            credito: this.detalle_credito.uuid,
            numero_credito: this.numero_credito,
            valor_desembolso: this.valor_desembolso,
            fecha_desembolso: this.formatearFecha(this.fecha_desembolso)
          }).then(_response => {
            this.$emit('emitCurrStateToParent', true)
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

    formatearFecha (fecha) {
      return fecha ? moment(fecha).format('YYYY-MM-DD') : null
    }
  },
  watch: {
    valor_desembolso () {
      if (this.valor_desembolso === 0) {
        this.disable = true
      }
      if (this.valor_desembolso > 0) {
        this.disable = false
      }
    }
  }
}
</script>
