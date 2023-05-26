import axios from 'axios'

export default ({ Vue, router, store }) => {
  axios.defaults.baseURL = process.env.API // se obtiene de quasar.conf.js
  axios.defaults.withCredentials = true

  axios.interceptors.request.use(function (config) {
    config.headers.authorization = 'JWT ' + store.state.auth.token
    return config
  })

  axios.interceptors.response.use(function (response) {
    let methodsMessages = ['post', 'put', 'delete']
    if (response.config.url === axios.defaults.baseURL + 'seguridad/login/') {
      // Uso de mensajes
    } else if (methodsMessages.includes(response.config.method) || response.config.url.includes('seguridad/usuarios/generar_clave/')) {
      Vue.swal.fire({
        customClass: {
          container: 'my-swal'
        },
        type: 'success',
        title: 'Proceso exitoso',
        showConfirmButton: false,
        timer: 1500
      })
    }
    return response
  }, function (error) {
    let errors = Object.entries(error.response.data)
    let str = ''
    if (error.response.status === 401) errors[0][1] = 'Sesión expirada, inicie sesión de nuevo.'
    for (const element of errors) {
      str += element[1] + '<br>'
    }
    Vue.swal.fire({
      customClass: {
        container: 'my-swal'
      },
      title: '<strong>Error <u></u></strong>',
      type: 'error',
      html: str,
      showCloseButton: true,
      focusConfirm: false,
      confirmButtonText:
        '<i class="fa fa-thumbs-up"></i> Aceptar',
      confirmButtonAriaLabel: 'Thumbs up, great!'
    }).then((result) => {
      if (result.value) {
        if (error.response.status === 401) {
          router.push({ name: 'login' })
        }
      }
    })
    return Promise.reject(error)
  })

  Vue.prototype.$axios = axios
}
