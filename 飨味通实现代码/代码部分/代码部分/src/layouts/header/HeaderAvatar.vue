<template>
  <a-dropdown>
    <div class="header-avatar" style="cursor: pointer">
      <a-avatar class="avatar" size="small" shape="circle" :src="getImagePath(user)"/>
      <span class="name">{{user.name}}</span>
    </div>
    <a-menu :class="['avatar-menu']" slot="overlay">
      <a-menu-item @click="gotoOrder">
        <a-icon type="file" />
        <span>我的订单</span>
      </a-menu-item>
      <a-menu-item @click="gotoProfile">
        <a-icon type="setting" />
        <span>账户管理</span>
      </a-menu-item>
      <a-menu-divider />
      <a-menu-item @click="logout">
        <a-icon style="margin-right: 8px;" type="poweroff" />
        <span>退出登录</span>
      </a-menu-item>
    </a-menu>
  </a-dropdown>
</template>

<script>
import {mapGetters} from 'vuex'
import {logout} from '@/services/user'

export default {
  name: 'HeaderAvatar',
  computed: {
    ...mapGetters('account', ['user']),
  },
  methods: {
    logout() {
      logout()
      this.$router.push('/login')
    },
    gotoOrder() {
      this.$router.push('/mine/order')
    },
    gotoProfile() {
      this.$router.push('/mine/profile')
    },
    getImagePath(user) {
      if (user.picUrl === 'default.jpg') {
        return require(`@/assets/img/${user.picUrl}`);
      } else {
        return user.picture;
      }
    },
  }
}
</script>

<style lang="less">
  .header-avatar{
    display: inline-flex;
    .avatar, .name{
      align-self: center;
    }
    .avatar{
      margin-right: 8px;
    }
    .name{
      font-weight: 500;
    }
  }
  .avatar-menu{
    width: 150px;
  }

</style>
