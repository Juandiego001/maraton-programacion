export default [
  {
    icon: 'mdi-view-dashboard',
    title: 'Administración',
    items: [
      {
        icon: 'mdi-view-dashboard-outline',
        title: 'Roles',
        to: '/administration/roles'
      },
      {
        icon: 'mdi-wallet-membership',
        title: 'Estudiantes',
        to: '/administration/students'
      },
      {
        icon: 'mdi-shield-account-variant-outline',
        title: 'Estructuras',
        to: '/administration/structures'
      },
      {
        icon: 'mdi-chart-timeline-variant',
        title: 'Temáticas',
        to: '/administration/topics'
      },
      {
        icon: 'mdi-chart-box-outline',
        title: 'Notificaciones',
        to: '/administration/notifications'
      }
    ]
  },
  {
    icon: 'mdi-account',
    title: 'Maratón',
    items: [
      {
        icon: 'mdi-shield-crown-outline',
        title: 'Competencias',
        to: '/users/contests'
      },
      {
        icon: 'mdi-account-circle-outline',
        title: 'Retos',
        to: '/users/challenges'
      },
      {
        icon: 'mdi-school',
        title: 'Soluciones',
        to: '/users/solutions'
      },
      {
        icon: 'mdi-school',
        title: 'Materiales',
        to: '/users/materials'
      }
    ]
  }
]
