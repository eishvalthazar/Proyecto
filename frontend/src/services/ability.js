import { defineAbility } from '@casl/ability'

export default defineAbility((can, cannot) => {
  can(
    [
      'create', 'read', 'update', 'delete', 'detail', 'finish'
    ],

    [
      'Usuarios'
    ]
  )
})
