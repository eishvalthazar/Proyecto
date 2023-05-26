<template>
    <q-card style="width: 1200px; max-width: 80vw;">
      <q-card-section class="row items-center">
        <div class="text-h5">Detalle del Credito</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>
      <q-banner class="bg-grey-3">
        <template v-slot:avatar>
          <q-icon name="assignment" color="primary" />
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
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, idx) in this.datos_credito" :key="idx">
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
                </tr>
              </tbody>
            </q-markup-table>
          </div>
        </q-form>
      </q-card-section>
    </q-card>
</template>

<script>
import axios from 'axios'
import { MENSUAL, TRIMESTRAL, SEMESTRAL } from '../constantes/Opciones'
export default {
  name: 'detallecredito',
  props: {
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
      datos_credito: []
    }
  },

  created () {
    this.crearDetalle()
  },

  methods: {

    crearDetalle () {
      axios.get('creditos/detalle-credito/' + this.creditoUuid + '/').then(response => {
        this.datos_credito = response.data
      })
    }
  }
}
</script>
