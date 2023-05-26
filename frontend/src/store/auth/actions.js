import axios from 'axios'

export function login ({ commit }, payload) {
  return new Promise((resolve, reject) => {
    axios.post('seguridad/login/', payload).then(({ data, status }) => {
      if (status === 200) {
        commit('setToken', data.token)
        commit('setRol', data.usuario.rol.codigo)
        resolve(true)
      }
    }).catch(error => {
      reject(error)
    })
  })
}

export function logout ({ commit }) {
  return new Promise((resolve, reject) => {
    commit('destroyToken')
    resolve(true)
  })
}
