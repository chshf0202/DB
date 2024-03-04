import TabsView from '@/layouts/tabs/TabsView'
import BlankView from '@/layouts/BlankView'

// 路由配置
const options = {
  routes: [
    {
      path: '/login',
      name: '登录页',
      component: () => import('@/pages/login')
    },
    {
      path: '/register',
      name: '注册页',
      component: () => import('@/pages/register')
    },
    {
      path: '*',
      name: '404',
      component: () => import('@/pages/exception/404'),
    },
    {
      path: '/403',
      name: '403',
      component: () => import('@/pages/exception/403'),
    },
    {
      path: '/',
      name: '首页',
      component: TabsView,
      redirect: '/login',
      children: [
        {
          path: 'demo',
          name: '主页',
          meta: {
            icon: 'dashboard'
          },
          component: () => import('@/pages/demo')
        },
        {
          path: 'dishes',
          name: '点菜',
          meta: {
            icon: 'form'
          },
          component: () => import('@/pages/dishes')
        },
        {
          path: 'rating',
          name: '评价',
          meta: {
            icon: 'star'
          },
          component: () => import('@/pages/rating'),
        },
        {
          path: 'mine', //暂定
          name: '我的',
          meta: {
            icon: 'flag'
          },
          component: BlankView,
          children: [
            {
              path: 'order',
              name: '订单',
              meta: {
                icon: 'file'
              },
              component: () => import('@/pages/order'),
            },
            {
              path: 'profile',
              name: '账户管理',
              meta: {
                icon: 'setting'
              },
              component: () => import('@/pages/profile'),
            },
          ]
        },
        {
          path: 'admin',
          name: '管理员页面',
          meta: {
            icon: 'user',
            requiredRole: 'admin'
          },
          component: () => import('@/pages/admin'),
        },
        {
          name: '验权页面',
          path: 'auth/demo',
          meta: {
            icon: 'file-ppt',
            authority: {
              permission: 'form',
              role: 'manager'
            },
            component: () => import('@/pages/demo')
          }
        }
      ]
    }
  ]
}

export default options
