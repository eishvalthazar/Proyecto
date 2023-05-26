export function setToken (state, Token) {
  state.token = Token
}

export function setRol (state, rol) {
  state.rol = rol
}

export function destroyToken (state) {
  state.token = null
}
