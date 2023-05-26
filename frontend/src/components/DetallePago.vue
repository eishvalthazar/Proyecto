<template>
  <div style="width: 1200px; max-width: 80vw;">
    <q-card style="width: 1200px; max-width: 80vw;">
      <q-card-section class="row items-center">
        <div class="text-h5">Detalle del Crédito</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>
      <q-banner class="bg-grey-3">
        <template v-slot:avatar>
          <q-icon name="assignment" color="info" />
        </template>
        A continuación verá la proyección del crédito
      </q-banner>
      <q-card-section>
        <q-form ref="form">
          <div class="q-pa-md">
            <q-markup-table>
              <thead>
                <tr>
                  <th scope="col" class="text-center">PAGO</th>
                  <th scope="col" class="text-center">MES</th>
                  <th scope="col" class="text-center">AÑO</th>
                  <th scope="col" class="text-center">DEUDA</th>
                  <th scope="col" class="text-center">INTERES</th>
                  <th scope="col" class="text-center">CAPITAL</th>
                  <th scope="col" class="text-center">CUOTA</th>
                  <th scope="col" class="text-center">SALDO</th>
                  <th scope="col" class="text-center">¿PAGÓ?</th>
                  <th scope="col" class="text-center">PAGAR</th>
                  <th scope="col" class="text-center">COMPROBANTE</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, idx) in datos_pago" :key="idx">
                  <td class="text-center">
                    {{row.pago}}
                  </td>
                  <td class="text-center">
                    {{row.mes}}
                  </td>
                  <td class="text-center">
                    {{row.anio}}
                  </td>
                  <td class="text-center">
                    {{row.deuda | currency }}
                  </td>
                  <td class="text-center">
                    {{row.interes | currency }}
                  </td>
                  <td class="text-center">
                    {{row.capital | currency }}
                  </td>
                  <td class="text-center">
                    {{row.cuota | currency }}
                  </td>
                  <td class="text-center">
                    {{row.saldo | currency }}
                  </td>
                  <td class="text-center">
                    {{ (row.pago_efectuado) ? 'SI' : 'NO' }}
                  </td>
                  <td class="text-center" key="pago">
                    <q-btn v-if="!row.pago_efectuado" round size="xs" color="amber" icon="payment" v-on:click="formatoPago(row)" />
                  </td>
                  <td class="text-center" key="exportar">
                    <q-btn v-if="row.pago_efectuado" round size="xs" color="green" icon="receipt_long" v-on:click="pagoPdf(row)" />
                  </td>
                </tr>
              </tbody>
            </q-markup-table>
          </div>
        </q-form>
      </q-card-section>
    </q-card>
    <q-dialog v-model="toolbar" persistent>
      <q-card style="width: 700px; max-width: 80vw;">
        <q-card-section class="row items-center">
          <div class="text-h6">Pago</div>
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
                <q-input readonly filled v-model="interes" label="Interes *" lazy-rules :rules="[ val => val && val.length > 0 || 'El campo es obligatorio']"/>
              </div>
              <div class="col-md-5">
                <q-input filled v-model="capital" label="Capital *" lazy-rules :rules="[ val => val && val.length > 0 || 'El campo es obligatorio']"/>
              </div>
              <div class="col-md-5">
                <q-input readonly filled v-model="cuota" label="Cuota *" lazy-rules :rules="[ val => val && val.length > 0 || 'El campo es obligatorio']"/>
              </div>
              <div class="col-md-5">
                <q-input readonly filled v-model="saldo" label="Saldo *" lazy-rules :rules="[ val => val && val.length > 0 || 'El campo es obligatorio']"/>
              </div>
              <div class="col-md-5">
                <q-radio filled size="xl" v-model="cambiar_tipo_anticipo" label="Anticipo a primer cuota" val="true" />
              </div>
              <div class="col-md-5">
                <q-radio filled size="xl" v-model="cambiar_tipo_anticipo" label="Anticipo a ultima cuota" val="false" />
              </div>
            </div>
          </q-form>
        </q-card-section>
        <q-card-actions align="right" class="bg-white text-teal">
          <q-btn label="Guardar" @click.prevent="guardarPago" color="primary"/>
          <q-btn label="Cancelar" v-close-popup color="negative"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import { MENSUAL, TRIMESTRAL, SEMESTRAL } from '../constantes/Opciones'
export default {
  name: 'detallepago',
  props: {
    desembolsoUuid: {
      type: String,
      required: true
    },
    creditoUuid: {
      type: String,
      required: true
    }
  },
  data () {
    return {
      mensual: MENSUAL,
      trimestral: TRIMESTRAL,
      semestral: SEMESTRAL,
      pago: null,
      interes: 0,
      capital: 0,
      cuota: 0,
      saldo: 0,
      interes_formato: 0,
      capital_formato: 0,
      cuota_formato: 0,
      saldo_formato: 0,
      saldo_fijo: 0,
      cuota_anticipo: 0,
      cambiar_tipo_anticipo: false,
      toolbar: false,
      detalle_pago: this.detallePago,
      detalle_credito: this.detallecredito,
      datos_pago: []
    }
  },

  mounted () {
    this.buscarDatosDesembolso()
  },

  methods: {
    buscarDatosDesembolso () {
      axios.get('creditos/desembolsos/obtener/' + this.creditoUuid + '/' + this.desembolsoUuid + '/').then(response => {
        this.datos_pago = response.data
      })
    },

    pagoPdf (row) {
      axios.get('pagos/descargar-pdf/' + row.uuid + '/').then(response => {
        // Converting the data in a PDF
        let fileURL = window.URL.createObjectURL(new Blob([response.data]))
        let fileLink = document.createElement('a')
        fileLink.href = fileURL
        // Getting the now Date
        let today = new Date()
        let date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate()
        // Downloading the document
        fileLink.setAttribute('download', `Orden-de-pago-${date}.pdf`)
        document.body.appendChild(fileLink)
        fileLink.click()
      })
    },

    formatoPago (row) {
      this.toolbar = true
      this.capital = row.capital
      this.cuota = row.cuota
      this.interes = row.interes
      this.anio = row.anio
      this.deuda = row.deuda
      this.mes = row.mes
      this.pago = row.pago
      this.saldo = row.saldo
      this.saldo_fijo = row.saldo
      this.desembolso = this.desembolsoUuid
      this.cuota_anticipo = row.cuota_anticipo
    },

    guardarPago () {
      let params = {
        anio: this.anio,
        capital: this.capital,
        cuota: this.cuota,
        deuda: this.deuda,
        interes: this.interes,
        mes: this.mes,
        pago: this.pago,
        saldo: this.saldo,
        cambiar_tipo_anticipo: this.cambiar_tipo_anticipo,
        desembolso: this.desembolsoUuid,
        cuota_anticipo: this.cuota_anticipo
      }
      this.$q.dialog({
        title: 'Confirmación',
        message: 'Desea guardar el pago?',
        ok: {
          label: 'Si',
          color: 'positive'
        },
        cancel: {
          label: 'No',
          color: 'negative'
        }
      }).onOk(() => {
        axios.post('pagos/', params).then(_response => {
          this.toolbar = false
          this.$emit('cerrarDetalle')
        })
      })
    }
  },
  watch: {
    capital () {
      this.cuota = (parseFloat(this.interes) + parseFloat(this.capital))
      this.cuota = (this.cuota).toFixed(3)
    },
    cuota () {
      this.saldo = (parseFloat(this.saldo_fijo) - parseFloat(this.capital))
      this.saldo = (this.saldo).toFixed(3)
    }
  }
}
</script>
