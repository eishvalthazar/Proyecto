import Vue from 'vue'
import { abilitiesPlugin, Can } from '@casl/vue'
import ability from '../services/ability.js'
window.ability = ability

Vue.component('Can', Can)
Vue.use(abilitiesPlugin, ability)
