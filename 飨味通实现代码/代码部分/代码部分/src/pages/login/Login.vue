<template>
  <common-layout>
    <div class="top">
      <div class="header">
        <img alt="logo" class="logo" src="@/assets/img/logo.png" />
        <span class="title">{{systemName}}</span>
      </div>
      <div class="desc">随时随地，“飨”吃就吃！</div>
    </div>
    <div class="login">
        <a-tabs size="large" :tabBarStyle="{textAlign: 'center'}" style="padding: 0 2px;">
          <a-tab-pane tab="账户密码登录" key="1">
            <a-form @submit="onSubmit1" :form="form1">
            <a-alert type="error" :closable="true" v-if="error" :message="error" @close='onClose' showIcon style="margin-bottom: 24px;" />
            <a-form-item>
              <a-input
                autocomplete="autocomplete"
                size="large"
                placeholder="admin"
                v-decorator="['name', {rules: [{ required: true, message: '请输入账户名', whitespace: true}]}]"
              >
                <a-icon slot="prefix" type="user" />
              </a-input>
            </a-form-item>
            <a-form-item>
              <a-input
                size="large"
                placeholder="******"
                autocomplete="autocomplete"
                type="password"
                v-decorator="['password', {rules: [{ required: true, message: '请输入密码', whitespace: true}]}]"
              >
                <a-icon slot="prefix" type="lock" />
              </a-input>
            </a-form-item>
              <a-form-item>
                <a-button :loading="logging" style="width: 100%;margin-top: 24px" size="large" htmlType="submit" type="primary">登录</a-button>
              </a-form-item>
            </a-form>
            <div>
              <router-link style="float: right" to="register" >注册账户</router-link>
            </div>
          </a-tab-pane>
          <a-tab-pane tab="手机号登录" key="2">
            <a-form @submit="onSubmit2" :form="form2">
            <a-alert type="error" :closable="true" v-if="error" :message="error" @close='onClose' showIcon style="margin-bottom: 24px;" />
            <a-form-item>
              <a-input
                  autocomplete="autocomplete"
                  size="large"
                  placeholder="mobile number"
                  v-decorator="['mobile number', {rules: [{ required: true, message: '请输入手机号', whitespace: true}]}]"
              >
                <a-icon slot="prefix" type="mobile" />
              </a-input>
            </a-form-item>
            <a-form-item>
              <a-input
                  size="large"
                  placeholder="******"
                  autocomplete="autocomplete"
                  type="password"
                  v-decorator="['password', {rules: [{ required: true, message: '请输入密码', whitespace: true}]}]"
              >
                <a-icon slot="prefix" type="lock" />
              </a-input>
            </a-form-item>
              <a-form-item>
                <a-button :loading="logging" style="width: 100%;margin-top: 24px" size="large" htmlType="submit" type="primary">登录</a-button>
              </a-form-item>
            </a-form>
            <div>
              <router-link style="float: right" to="register" >注册账户</router-link>
            </div>
          </a-tab-pane>
        </a-tabs>
    </div>
  </common-layout>
</template>

<script>
import CommonLayout from '@/layouts/CommonLayout'
// import {login, getRoutesConfig} from '@/services/user'
import {getRoutesConfig} from '@/services/user'
import {setAuthorization} from '@/utils/request'
import {loadRoutes} from '@/utils/routerUtil'
import {mapMutations} from 'vuex'
import axios from 'axios';

export default {
  name: 'Login',
  components: {CommonLayout},
  data () {
    return {
      logging: false,
      error: '',
      form1: this.$form.createForm(this),
      form2: this.$form.createForm(this),
    }
  },
  computed: {
    systemName () {
      return this.$store.state.setting.systemName
    }
  },
  methods: {
    ...mapMutations('account', ['setUser', 'setPermissions', 'setRoles']),
    onSubmit1 (e) {
      e.preventDefault()
      this.form1.validateFields((err) => {
        if (!err) {
          this.logging = true
          const name = this.form1.getFieldValue('name')
          const password = this.form1.getFieldValue('password')
            axios.post(`LoginUserName/`, {
              Uname: name,
              pwd: password,
            })
                .then(response => {
                  this.afterLogin(response);
                })

          // login(name, password).then(this.afterLogin)
        }
      })
    },
    onSubmit2 (e) {
      e.preventDefault()
      this.form2.validateFields((err) => {
        if (!err) {
          this.logging = true
          const password = this.form2.getFieldValue('password')
          const phone = this.form2.getFieldValue('mobile number')
            axios.post(`LoginUserPhone/`, {
              phone: phone,
              pwd: password,
            })
                .then(response => {
                  this.afterLogin(response);
                })

          // login(name, password).then(this.afterLogin)
        }
      })
    },
    afterLogin(res) {
      this.logging = false
      const loginRes = res.data
      if (loginRes.value === 0) {
        const {user, permissions, roles} = loginRes.data
        if (loginRes.data.user.picture == null) {
            user['picUrl'] = 'default.jpg'
      }
        //this.$message.success(roles)
      this.setUser(user)
        this.setPermissions(permissions)
        this.setRoles(roles)
        setAuthorization({token: loginRes.data.token, expireAt: new Date(loginRes.data.expireAt)})
        // 获取路由配置
        getRoutesConfig().then(result => {
          const routesConfig = result.data
          loadRoutes(routesConfig)
          this.$router.push('/demo')
          this.$message.success(loginRes.message, 3)
        })
      } else {
        this.error = loginRes.message
      }
    },
    onClose() {
      this.error = false
    }
  }
}
</script>

<style lang="less" scoped>
  .common-layout{
    .top {
      text-align: center;
      .header {
        height: 44px;
        line-height: 44px;
        a {
          text-decoration: none;
        }
        .logo {
          height: 44px;
          vertical-align: top;
          margin-right: 16px;
        }
        .title {
          font-size: 33px;
          color: @title-color;
          font-family: 'Myriad Pro', 'Helvetica Neue', Arial, Helvetica, sans-serif;
          font-weight: 600;
          position: relative;
          top: 2px;
        }
      }
      .desc {
        font-size: 14px;
        color: @text-color-second;
        margin-top: 12px;
        margin-bottom: 40px;
      }
    }
    .login{
      width: 368px;
      margin: 0 auto;
      @media screen and (max-width: 576px) {
        width: 95%;
      }
      //@media screen and (max-width: 320px) {
      //  .captcha-button{
      //    font-size: 14px;
      //  }
      //}
      .icon {
        font-size: 24px;
        color: @text-color-second;
        margin-left: 16px;
        vertical-align: middle;
        cursor: pointer;
        transition: color 0.3s;

        &:hover {
          color: @primary-color;
        }
      }
    }
  }
</style>
