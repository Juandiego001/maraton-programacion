export default [
  {
    icon: 'mdi-view-dashboard',
    title: 'Administración',
    items: [
      {
        icon: 'mdi-shield-account-variant-outline',
        title: 'Roles',
        to: '/administration/roles'
      },
      {
        icon: 'mdi-account',
        title: 'Usuarios',
        to: '/administration/users'
      },
      {
        icon: 'mdi-tag-multiple-outline',
        title: 'Temáticas',
        to: '/administration/topics'
      },
      {
        icon: 'mdi-lan',
        title: 'Estructuras',
        to: '/administration/structures'
      },
      {
        icon: 'mdi-bell-outline',
        title: 'Notificaciones',
        to: '/administration/notifications'
      }
    ]
  },
  {
    icon: 'mdi-alpha-m-box-outline',
    title: 'Maratón',
    items: [
      {
        icon: 'mdi-medal-outline',
        title: 'Competencias',
        to: '/marathon/contests'
      },
      {
        icon: 'mdi-text-box-outline',
        title: 'Retos',
        to: '/marathon/challenges'
      },
      {
        icon: 'mdi-code-tags',
        title: 'Soluciones',
        to: '/marathon/solutions'
      },
      {
        icon: 'mdi-book',
        title: 'Materiales',
        to: '/marathon/materials'
      }
    ]
  }
]
